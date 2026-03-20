#!/usr/bin/env bash
# =============================================================================
# run_trace.sh — Run QuickSort with --trace on all test_input files
#
# For each input file in test_input/, runs four combinations:
#   - default partition
#   - median-of-three partition
#   each capturing both stdout (sorted output + trace lines) and
#   stderr (partition call count summary) into a single .txt file
#   in trace_output/.
#
# Output file naming:
#   one_million_random_ints.csv  →  one_million_random-default.txt
#                                   one_million_random-median-of-three.txt
#   one_million_sorted_ints.csv  →  one_million_sorted-default.txt
#                                   one_million_sorted-median-of-three.txt
#
# Stack size:
#   Uses -Xss2g for all runs — sufficient for n=10,000,000 worst-case depth.
#
# Trace threshold:
#   --trace produces one line per partition call (n-1 lines total).
#   For large inputs this generates gigabytes of output and takes a very long
#   time to write. Files above TRACE_SIZE_LIMIT bytes will be run WITHOUT
#   --trace — only the stderr partition call count summary is captured.
#   Set TRACE_SIZE_LIMIT=0 to force --trace on all files (not recommended).
#
# Usage:
#   chmod +x run_trace.sh
#   ./run_trace.sh
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

INPUT_DIR="test_input"
OUTPUT_DIR="trace_output"
JAVA_STACK="-Xss512m"
PARTITIONS=("default" "median-of-three")

# Files larger than this (in bytes) will skip --trace and only capture the
# stderr summary. 100 KB = 102400 bytes — covers up to ~ten_thousand files.
# Increase to e.g. 6000000 (6 MB) to include one_hundred_thousand files.
TRACE_SIZE_LIMIT=102400

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

mkdir -p "$OUTPUT_DIR"

if [ ! -d "$INPUT_DIR" ]; then
    echo "ERROR: input directory '$INPUT_DIR' not found." >&2
    exit 1
fi

# Collect all CSV files sorted by size (smallest first)
mapfile -t INPUT_FILES < <(find "$INPUT_DIR" -name "*.csv" | sort)

if [ ${#INPUT_FILES[@]} -eq 0 ]; then
    echo "ERROR: no .csv files found in '$INPUT_DIR'." >&2
    exit 1
fi

total_runs=$(( ${#INPUT_FILES[@]} * ${#PARTITIONS[@]} ))
run_number=0

echo "============================================="
echo " QuickSort Trace Runner"
echo "============================================="
echo " Input dir  : $INPUT_DIR"
echo " Output dir : $OUTPUT_DIR"
echo " Stack size : $JAVA_STACK"
echo " Trace limit: files > $TRACE_SIZE_LIMIT bytes will skip --trace"
echo " Total runs : $total_runs"
echo "============================================="
echo ""

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

for input_file in "${INPUT_FILES[@]}"; do

    # Derive base name: strip directory and _ints.csv suffix
    # e.g. test_input/one_million_random_ints.csv → one_million_random
    filename=$(basename "$input_file")             # one_million_random_ints.csv
    base="${filename%_ints.csv}"                   # one_million_random

    # Determine file size for trace threshold decision
    file_size=$(wc -c < "$input_file")

    for partition in "${PARTITIONS[@]}"; do

        run_number=$(( run_number + 1 ))
        output_file="$OUTPUT_DIR/${base}-${partition}.txt"

        # Decide whether to use --trace based on file size
        if [ "$TRACE_SIZE_LIMIT" -gt 0 ] && [ "$file_size" -gt "$TRACE_SIZE_LIMIT" ]; then
            trace_flag=""
            trace_note="(trace skipped — file too large, stderr summary only)"
        else
            trace_flag="--trace"
            trace_note="(full trace)"
        fi

        echo "[$run_number/$total_runs] partition=$partition  file=$filename  $trace_note"
        echo "  → $output_file"

        # Build the command
        # --suppress is NOT used so the sorted output is also captured
        # Both stdout and stderr are merged into the output file so the
        # partition call count summary appears alongside the trace lines
        cmd="java $JAVA_STACK QuickSort \
            --partition $partition \
            $trace_flag \
            --file $input_file"

        # Write a header into the output file
        {
            echo "============================================="
            echo " QuickSort Trace Output"
            echo "============================================="
            echo " Input file : $input_file"
            echo " Partition  : $partition"
            echo " File size  : $file_size bytes"
            echo " Trace      : ${trace_flag:-(disabled — file too large)}"
            echo " Command    : $cmd"
            echo " Timestamp  : $(date)"
            echo "============================================="
            echo ""
        } > "$output_file"

        # Run QuickSort, merging stdout and stderr into the output file
        # The 2>&1 redirect ensures the stderr partition count summary
        # (always printed regardless of --trace) is captured alongside
        # the sorted output and any trace lines
        if java $JAVA_STACK QuickSort \
                --partition "$partition" \
                $trace_flag \
                --file "$input_file" >> "$output_file" 2>&1; then
            echo "  ✓ done"
        else
            echo "  ✗ FAILED (exit code $?) — see $output_file for details"
        fi

        echo ""

    done
done

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

echo "============================================="
echo " All $total_runs runs complete."
echo " Output written to: $OUTPUT_DIR/"
echo "============================================="
echo ""
echo "Files written:"
ls -lh "$OUTPUT_DIR/"
