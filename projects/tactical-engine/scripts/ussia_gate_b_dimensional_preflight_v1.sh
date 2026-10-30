#!/usr/bin/env bash
#
# USSIA Gate B — preflight dimensionale metadata-only
#
# VERSIONE DERIVATA: USSIA_GATE_B_DIMENSIONAL_PREFLIGHT_DERIVED_05
# DERIVATA DA: USSIA_GATE_B_DIMENSIONAL_PREFLIGHT_DERIVED_04
# ORIGINALE STORICO:
#   SHA-256 fd77fa0e08a9e2d745849cafa8133de946c06bf50839d80ea67af27b4fdd21e5
#
# STATO: PROPOSTO, NON AUTORIZZATO, NON ESEGUITO
#
# Exit code:
#   0  COMPLETE_CAPACITY_PASS
#   2  INCOMPLETE
#   3  COMPLETE_CAPACITY_FAIL
#  10  NOT_DETERMINABLE: percorso o symlink
#  20  NOT_DETERMINABLE: metadati, filesystem o aritmetica
#  30  NOT_DETERMINABLE: mount
#  40  NOT_DETERMINABLE: dimensioni
#  50  NOT_DETERMINABLE: scansione strutturale o errore inatteso
#
# Il completamento del preflight non autorizza la cold copy.

set -euo pipefail
export LC_ALL=C

readonly CHROMA='/opt/football-data-lab/knowledge/rag/chroma'
readonly STAGING_PARENT='/home/football/.local/share/football-data-lab/evidence'
readonly INT64_MAX='9223372036854775807'
readonly GIB='1073741824'
readonly MINIMUM_INODE_RESERVE='10000'

RESULT_EMITTED=0

emit_safety_markers() {
    printf '%s\n' 'temporal_consistency_proven=no'
    printf '%s\n' 'staging_write_verified=no'
    printf '%s\n' 'duration_status=NOT_DETERMINABLE'
    printf '%s\n' 'cold_copy_authorized=no'
}

on_exit() {
    local original_status=$?
    local final_status=$original_status

    trap - EXIT HUP INT TERM

    if [ "$RESULT_EMITTED" -eq 0 ]; then
        printf '%s\n' \
            'result=NOT_DETERMINABLE|reason=unexpected_or_unclassified_error'
        final_status=50
    fi

    emit_safety_markers
    exit "$final_status"
}

finish_result() {
    local code=$1
    local result=$2

    RESULT_EMITTED=1
    printf 'result=%s\n' "$result"
    exit "$code"
}

fail_not_determinable() {
    local code=$1
    local reason=$2

    finish_result \
        "$code" \
        "NOT_DETERMINABLE|reason=${reason}"
}

on_signal() {
    local signal_name=$1

    finish_result \
        50 \
        "NOT_DETERMINABLE|reason=interrupted_by_${signal_name}"
}

trap on_exit EXIT
trap 'on_signal hup' HUP
trap 'on_signal int' INT
trap 'on_signal term' TERM

normalize_uint64_into() {
    local destination=$1
    local raw=${2-}
    local normalized

    case "$raw" in
        ''|*[!0-9]*)
            return 1
            ;;
    esac

    normalized=$raw

    while [ "${#normalized}" -gt 1 ] &&
          [ "${normalized#0}" != "$normalized" ]; do
        normalized=${normalized#0}
    done

    if [ "${#normalized}" -gt "${#INT64_MAX}" ]; then
        return 1
    fi

    if [ "${#normalized}" -eq "${#INT64_MAX}" ] &&
       [[ "$normalized" > "$INT64_MAX" ]]; then
        return 1
    fi

    printf -v "$destination" '%s' "$normalized"
}

safe_add_into() {
    local destination=$1
    local left_raw=$2
    local right_raw=$3
    local left
    local right
    local maximum_left

    normalize_uint64_into left "$left_raw" || return 1
    normalize_uint64_into right "$right_raw" || return 1

    maximum_left=$((10#$INT64_MAX - 10#$right))

    if [ $((10#$left)) -gt "$maximum_left" ]; then
        return 1
    fi

    printf -v "$destination" \
        '%s' \
        "$((10#$left + 10#$right))"
}

safe_ceil_percent_into() {
    local destination=$1
    local value_raw=$2
    local percent_raw=$3
    local value
    local percent
    local quotient
    local remainder
    local quotient_product
    local remainder_product
    local remainder_ceil
    local result

    normalize_uint64_into value "$value_raw" || return 1
    normalize_uint64_into percent "$percent_raw" || return 1

    quotient=$((10#$value / 100))
    remainder=$((10#$value % 100))

    if [ "$percent" -ne 0 ] &&
       [ "$quotient" -gt $((10#$INT64_MAX / 10#$percent)) ]; then
        return 1
    fi

    quotient_product=$((quotient * 10#$percent))

    if [ "$percent" -ne 0 ] &&
       [ "$remainder" -gt $((10#$INT64_MAX / 10#$percent)) ]; then
        return 1
    fi

    remainder_product=$((remainder * 10#$percent))

    if [ "$remainder_product" -gt $((10#$INT64_MAX - 99)) ]; then
        return 1
    fi

    remainder_ceil=$(((remainder_product + 99) / 100))

    safe_add_into \
        result \
        "$quotient_product" \
        "$remainder_ceil" ||
        return 1

    printf -v "$destination" '%s' "$result"
}

max_uint64_into() {
    local destination=$1
    local left_raw=$2
    local right_raw=$3
    local left
    local right

    normalize_uint64_into left "$left_raw" || return 1
    normalize_uint64_into right "$right_raw" || return 1

    if [ $((10#$left)) -ge $((10#$right)) ]; then
        printf -v "$destination" '%s' "$left"
    else
        printf -v "$destination" '%s' "$right"
    fi
}

normalize_or_fail() {
    local destination=$1
    local raw=$2
    local reason=$3

    if ! normalize_uint64_into "$destination" "$raw"; then
        fail_not_determinable 20 "$reason"
    fi
}

safe_add_or_fail() {
    local destination=$1
    local left=$2
    local right=$3
    local reason=$4

    if ! safe_add_into "$destination" "$left" "$right"; then
        fail_not_determinable 20 "$reason"
    fi
}

safe_structure_add_or_fail() {
    local destination=$1
    local left=$2
    local right=$3
    local reason=$4

    if ! safe_add_into "$destination" "$left" "$right"; then
        fail_not_determinable 50 "$reason"
    fi
}

safe_percent_or_fail() {
    local destination=$1
    local value=$2
    local percent=$3
    local reason=$4

    if ! safe_ceil_percent_into \
        "$destination" \
        "$value" \
        "$percent"; then
        fail_not_determinable 20 "$reason"
    fi
}

max_uint64_or_fail() {
    local destination=$1
    local left=$2
    local right=$3
    local reason=$4

    if ! max_uint64_into "$destination" "$left" "$right"; then
        fail_not_determinable 20 "$reason"
    fi
}

check_single_line() {
    local value=${1-}
    local reason=$2

    if [ -z "$value" ]; then
        fail_not_determinable 20 "${reason}_empty"
    fi

    case "$value" in
        *$'\n'*|*$'\r'*)
            fail_not_determinable \
                20 \
                "${reason}_unexpected_cardinality"
            ;;
    esac
}

check_components_without_following_symlinks() {
    local role=$1
    shift

    local index=0
    local component

    for component in "$@"; do
        index=$((index + 1))

        if [ -L "$component" ]; then
            fail_not_determinable \
                10 \
                "${role}_component_${index}_is_symlink"
        fi

        if [ ! -e "$component" ]; then
            fail_not_determinable \
                10 \
                "${role}_component_${index}_missing"
        fi
    done

    printf 'component_check|role=%s|result=pass\n' "$role"
}

readonly INTERNAL_MOUNT_AWK='
    index($0, root "/") == 1 {
        count++
    }

    END {
        print count + 0
    }
'

readonly DF_SPACE_AWK='
    NR == 1 {
        header_count=NF

        if (NF != 2 ||
            $1 != "1B-blocks" ||
            $2 != "Avail")
            invalid=1

        next
    }

    NR == 2 {
        if (NF != 2) {
            invalid=1
        } else if ($1 !~ /^[0-9]+$/ ||
                   $2 !~ /^[0-9]+$/) {
            invalid=1
        } else {
            total=$1
            available=$2
            data_rows++
        }

        next
    }

    {
        invalid=1
    }

    END {
        if (header_count != 2 || data_rows != 1)
            invalid=1

        if (invalid) {
            exit 14
        } else {
            print total, available
        }
    }
'

readonly DF_INODE_AWK='
    NR == 1 {
        header_count=NF

        if (NF != 2 ||
            $1 != "Inodes" ||
            $2 != "IFree")
            invalid=1

        next
    }

    NR == 2 {
        if (NF != 2) {
            invalid=1
        } else if ($1 !~ /^[0-9]+$/ ||
                   $2 !~ /^[0-9]+$/) {
            invalid=1
        } else {
            total=$1
            available=$2
            data_rows++
        }

        next
    }

    {
        invalid=1
    }

    END {
        if (header_count != 2 || data_rows != 1)
            invalid=1

        if (invalid) {
            exit 14
        } else {
            print total, available
        }
    }
'

readonly DU_AWK='
    {
        if (NR != 1 || NF < 2 || $1 !~ /^[0-9]+$/) {
            invalid=1
        } else {
            value=$1
            rows++
        }
    }

    END {
        if (rows != 1)
            invalid=1

        if (invalid) {
            exit 14
        } else {
            print value
        }
    }
'

readonly STRUCTURE_AWK='
    BEGIN {
        max_exact="9007199254740991"
        max_identity_groups="1000000"

        valid_type["f"]=1
        valid_type["d"]=1
        valid_type["l"]=1
        valid_type["b"]=1
        valid_type["c"]=1
        valid_type["p"]=1
        valid_type["s"]=1
        valid_type["D"]=1
    }

    function normalize_decimal(value, normalized) {
        normalized=value
        sub(/^0+/, "", normalized)

        if (normalized == "")
            normalized="0"

        return normalized
    }

    function decimal_compare(left, right) {
        left=normalize_decimal(left)
        right=normalize_decimal(right)

        if (length(left) < length(right))
            return -1

        if (length(left) > length(right))
            return 1

        if (("x" left) < ("x" right))
            return -1

        if (("x" left) > ("x" right))
            return 1

        return 0
    }

    function is_exact_counter(value) {
        value=normalize_decimal(value)
        return decimal_compare(value, max_exact) <= 0
    }

    function increment_exact(current, i, digit, carry, result) {
        current=normalize_decimal(current)

        if (!is_exact_counter(current)) {
            numeric_unverifiable=1
            return current
        }

        carry=1
        result=""

        for (i=length(current); i>=1; i--) {
            digit=substr(current, i, 1) + carry

            if (digit >= 10) {
                digit-=10
                carry=1
            } else {
                carry=0
            }

            result=digit result
        }

        if (carry)
            result="1" result

        result=normalize_decimal(result)

        if (!is_exact_counter(result)) {
            numeric_unverifiable=1
            return current
        }

        return result
    }

    function exact_decimal_equal(left, right) {
        return decimal_compare(left, right) == 0
    }

    {
        if (NF != 4) {
            malformed=1
            next
        }

        record_type=$1
        device_text=$2
        inode_text=$3
        links_text=$4

        if (!(record_type in valid_type)) {
            malformed=1
            next
        }

        if (device_text !~ /^[0-9]+$/ ||
            inode_text !~ /^[0-9]+$/ ||
            links_text !~ /^[0-9]+$/) {
            malformed=1
            next
        }

        links_text=normalize_decimal(links_text)

        if (exact_decimal_equal(links_text, "0")) {
            malformed=1
            next
        }

        if (!is_exact_counter(links_text)) {
            numeric_unverifiable=1
            next
        }

        type_count[record_type]=increment_exact(
            type_count[record_type]
        )

        object_count=increment_exact(object_count)

        if (record_type == "f") {
            key="device:" substr("x" device_text, 2) \
                "|inode:" substr("x" inode_text, 2)

            if (!(key in declared_links)) {
                next_identity_group_count=increment_exact(
                    identity_group_count
                )

                if (numeric_unverifiable ||
                    decimal_compare(
                        next_identity_group_count,
                        max_identity_groups
                    ) > 0) {
                    identity_resource_limit=1
                    next
                }

                identity_group_count=next_identity_group_count
                declared_links[key]=links_text
            }

            observed_links[key]=increment_exact(
                observed_links[key]
            )

            if (!exact_decimal_equal(
                declared_links[key],
                links_text
            )) {
                declared_mismatch[key]=1
            }
        }
    }

    END {
        internal_complete=0
        external_not_resolved=0
        inconsistent=0

        if (!malformed &&
            !numeric_unverifiable &&
            !identity_resource_limit) {
            for (key in observed_links) {
                if (declared_mismatch[key]) {
                    inconsistent=increment_exact(inconsistent)
                } else if (decimal_compare(
                    observed_links[key],
                    declared_links[key]
                ) > 0) {
                    inconsistent=increment_exact(inconsistent)
                } else if (exact_decimal_equal(
                    declared_links[key],
                    "1"
                ) && exact_decimal_equal(
                    observed_links[key],
                    "1"
                )) {
                    # File regolare ordinario: non è un gruppo hard link.
                } else if (decimal_compare(
                    observed_links[key],
                    declared_links[key]
                ) < 0) {
                    external_not_resolved=increment_exact(
                        external_not_resolved
                    )
                } else {
                    internal_complete=increment_exact(
                        internal_complete
                    )
                }
            }
        }

        if (malformed) {
            exit 21
        } else if (identity_resource_limit) {
            exit 23
        } else if (numeric_unverifiable) {
            exit 22
        } else {
            print "object_count=" normalize_decimal(object_count)
            print "type_count|type=f|count=" \
                normalize_decimal(type_count["f"])
            print "type_count|type=d|count=" \
                normalize_decimal(type_count["d"])
            print "type_count|type=l|count=" \
                normalize_decimal(type_count["l"])
            print "type_count|type=b|count=" \
                normalize_decimal(type_count["b"])
            print "type_count|type=c|count=" \
                normalize_decimal(type_count["c"])
            print "type_count|type=p|count=" \
                normalize_decimal(type_count["p"])
            print "type_count|type=s|count=" \
                normalize_decimal(type_count["s"])
            print "type_count|type=D|count=" \
                normalize_decimal(type_count["D"])

            print "hardlink_summary" \
                  "|internal_complete=" \
                      normalize_decimal(internal_complete) \
                  "|external_not_resolved=" \
                      normalize_decimal(external_not_resolved) \
                  "|inconsistent=" normalize_decimal(inconsistent)
        }
    }
'

readonly STRUCTURE_VALIDATE_AWK='
    function valid_uint(value) {
        return value ~ /^[0-9]+$/
    }

    $0 ~ /^object_count=/ {
        object_seen++

        split($0, fields, "=")

        if (length(fields) != 2 || !valid_uint(fields[2]))
            invalid=1

        object_value=fields[2]
        next
    }

    $0 ~ /^type_count\|type=/ {
        split($0, fields, "[|=]")

        if (length(fields) != 5 ||
            fields[1] != "type_count" ||
            fields[2] != "type" ||
            fields[4] != "count" ||
            !valid_uint(fields[5])) {
            invalid=1
            next
        }

        type_name=fields[3]

        if (type_name != "f" &&
            type_name != "d" &&
            type_name != "l" &&
            type_name != "b" &&
            type_name != "c" &&
            type_name != "p" &&
            type_name != "s" &&
            type_name != "D") {
            invalid=1
            next
        }

        type_seen[type_name]++
        type_value[type_name]=fields[5]
        next
    }

    $0 ~ /^hardlink_summary\|/ {
        hardlink_seen++

        split($0, fields, "[|=]")

        if (length(fields) != 7 ||
            fields[1] != "hardlink_summary" ||
            fields[2] != "internal_complete" ||
            fields[4] != "external_not_resolved" ||
            fields[6] != "inconsistent" ||
            !valid_uint(fields[3]) ||
            !valid_uint(fields[5]) ||
            !valid_uint(fields[7])) {
            invalid=1
            next
        }

        hardlink_internal=fields[3]
        hardlink_external=fields[5]
        hardlink_inconsistent=fields[7]
        next
    }

    {
        invalid=1
    }

    END {
        required_types[1]="f"
        required_types[2]="d"
        required_types[3]="l"
        required_types[4]="b"
        required_types[5]="c"
        required_types[6]="p"
        required_types[7]="s"
        required_types[8]="D"

        if (object_seen != 1 || hardlink_seen != 1)
            invalid=1

        for (i=1; i<=8; i++) {
            type_name=required_types[i]

            if (type_seen[type_name] != 1)
                invalid=1
        }

        if (NR != 10)
            invalid=1

        if (invalid) {
            exit 31
        } else {
            print object_value
            print type_value["f"]
            print type_value["d"]
            print type_value["l"]
            print type_value["b"]
            print type_value["c"]
            print type_value["p"]
            print type_value["s"]
            print type_value["D"]
            print hardlink_internal
            print hardlink_external
            print hardlink_inconsistent
        }
    }
'

printf '%s\n' 'activity=USSIA_GATE_B_DIMENSIONAL_PREFLIGHT'
printf '%s\n' \
    'artifact_version=USSIA_GATE_B_DIMENSIONAL_PREFLIGHT_DERIVED_05'
printf '%s\n' \
    'baseline=23508fc3a7bb4f0b33ab95687ae5d55b6c6be6ab'
printf '%s\n' 'execution_mode=metadata_only'
printf '%s\n' 'section=path_identity'

check_components_without_following_symlinks \
    chroma \
    /opt \
    /opt/football-data-lab \
    /opt/football-data-lab/knowledge \
    /opt/football-data-lab/knowledge/rag \
    /opt/football-data-lab/knowledge/rag/chroma

check_components_without_following_symlinks \
    staging_parent \
    /home \
    /home/football \
    /home/football/.local \
    /home/football/.local/share \
    /home/football/.local/share/football-data-lab \
    /home/football/.local/share/football-data-lab/evidence

if [ ! -d "$CHROMA" ]; then
    fail_not_determinable 10 'chroma_not_directory'
fi

if [ ! -d "$STAGING_PARENT" ]; then
    fail_not_determinable 10 'staging_parent_not_directory'
fi

if ! CHROMA_ID_BEFORE=$(
    stat -c '%d:%i:%Z:%Y' -- "$CHROMA" 2>/dev/null
); then
    fail_not_determinable 20 'chroma_initial_stat_failed'
fi

if ! STAGING_ID_BEFORE=$(
    stat -c '%d:%i:%Z:%Y' -- "$STAGING_PARENT" 2>/dev/null
); then
    fail_not_determinable 20 'staging_initial_stat_failed'
fi

if ! stat -c \
    'path_role=chroma|type=%F' \
    -- "$CHROMA" 2>/dev/null
then
    fail_not_determinable 20 'chroma_stat_failed'
fi

if ! stat -c \
    'path_role=staging_parent|type=%F' \
    -- "$STAGING_PARENT" 2>/dev/null
then
    fail_not_determinable 20 'staging_stat_failed'
fi

if [ -r "$CHROMA" ] && [ -x "$CHROMA" ]; then
    printf '%s\n' 'chroma_observed_access=readable_traversable'
else
    fail_not_determinable 20 'chroma_access_insufficient'
fi

STAGING_ACCESS_BLOCK=0

if [ -r "$STAGING_PARENT" ] &&
   [ -w "$STAGING_PARENT" ] &&
   [ -x "$STAGING_PARENT" ]; then
    printf '%s\n' \
        'staging_observed_access=readable_writable_traversable'
else
    printf '%s\n' 'staging_observed_access=insufficient'
    STAGING_ACCESS_BLOCK=1
fi

printf '%s\n' 'section=mount_boundaries'

if ! INTERNAL_MOUNT_COUNT=$(
    timeout --signal=TERM --kill-after=5s 15s \
        bash -o pipefail -c '
            findmnt -rn --raw -o TARGET 2>/dev/null |
                awk -v root="$1" "$2"
        ' bash "$CHROMA" "$INTERNAL_MOUNT_AWK" 2>/dev/null
); then
    fail_not_determinable 30 'internal_mount_detection_failed'
fi

normalize_or_fail \
    INTERNAL_MOUNT_COUNT \
    "$INTERNAL_MOUNT_COUNT" \
    'internal_mount_count_invalid'

printf 'internal_mount_count=%s\n' "$INTERNAL_MOUNT_COUNT"

if [ "$INTERNAL_MOUNT_COUNT" -ne 0 ]; then
    fail_not_determinable 30 'internal_mount_present'
fi

printf '%s\n' \
    'find_xdev_limit=bind_mount_same_device_not_proven_absent_by_xdev_alone'

printf '%s\n' 'section=filesystem'

if ! stat -f -c \
    'path_role=chroma|filesystem_type=%T|block_size=%S|fundamental_block=%s' \
    -- "$CHROMA" 2>/dev/null
then
    fail_not_determinable 20 'chroma_filesystem_stat_failed'
fi

if ! stat -f -c \
    'path_role=staging_parent|filesystem_type=%T|block_size=%S|fundamental_block=%s' \
    -- "$STAGING_PARENT" 2>/dev/null
then
    fail_not_determinable 20 'staging_filesystem_stat_failed'
fi

if ! CHROMA_DEVICE=$(stat -c '%d' -- "$CHROMA" 2>/dev/null); then
    fail_not_determinable 20 'chroma_device_unavailable'
fi

if ! STAGING_DEVICE=$(
    stat -c '%d' -- "$STAGING_PARENT" 2>/dev/null
); then
    fail_not_determinable 20 'staging_device_unavailable'
fi

normalize_or_fail \
    CHROMA_DEVICE \
    "$CHROMA_DEVICE" \
    'chroma_device_invalid'

normalize_or_fail \
    STAGING_DEVICE \
    "$STAGING_DEVICE" \
    'staging_device_invalid'

if [ "$CHROMA_DEVICE" = "$STAGING_DEVICE" ]; then
    SAME_FILESYSTEM=yes
else
    SAME_FILESYSTEM=no
fi

printf 'same_filesystem=%s\n' "$SAME_FILESYSTEM"

if ! FS_SPACE=$(
    timeout --signal=TERM --kill-after=5s 15s \
        bash -o pipefail -c '
            df -B1 --output=size,avail -- "$1" 2>/dev/null |
                awk "$2"
        ' bash "$STAGING_PARENT" "$DF_SPACE_AWK" 2>/dev/null
); then
    fail_not_determinable 20 'filesystem_capacity_unavailable'
fi

read -r FILESYSTEM_TOTAL_BYTES FILESYSTEM_AVAILABLE_BYTES <<EOF
$FS_SPACE
EOF

normalize_or_fail \
    FILESYSTEM_TOTAL_BYTES \
    "$FILESYSTEM_TOTAL_BYTES" \
    'filesystem_total_bytes_invalid'

normalize_or_fail \
    FILESYSTEM_AVAILABLE_BYTES \
    "$FILESYSTEM_AVAILABLE_BYTES" \
    'filesystem_available_bytes_invalid'

if [ "$FILESYSTEM_AVAILABLE_BYTES" -gt "$FILESYSTEM_TOTAL_BYTES" ]; then
    fail_not_determinable \
        20 \
        'filesystem_available_exceeds_total'
fi

printf 'filesystem_total_bytes=%s\n' "$FILESYSTEM_TOTAL_BYTES"
printf 'filesystem_available_bytes=%s\n' "$FILESYSTEM_AVAILABLE_BYTES"

if ! FS_INODES=$(
    timeout --signal=TERM --kill-after=5s 15s \
        bash -o pipefail -c '
            df -i --output=itotal,iavail -- "$1" 2>/dev/null |
                awk "$2"
        ' bash "$STAGING_PARENT" "$DF_INODE_AWK" 2>/dev/null
); then
    fail_not_determinable 20 'filesystem_inode_capacity_unavailable'
fi

read -r FILESYSTEM_TOTAL_INODES FILESYSTEM_FREE_INODES <<EOF
$FS_INODES
EOF

normalize_or_fail \
    FILESYSTEM_TOTAL_INODES \
    "$FILESYSTEM_TOTAL_INODES" \
    'filesystem_total_inodes_invalid'

normalize_or_fail \
    FILESYSTEM_FREE_INODES \
    "$FILESYSTEM_FREE_INODES" \
    'filesystem_free_inodes_invalid'

if [ "$FILESYSTEM_FREE_INODES" -gt "$FILESYSTEM_TOTAL_INODES" ]; then
    fail_not_determinable \
        20 \
        'filesystem_free_inodes_exceed_total'
fi

printf 'filesystem_total_inodes=%s\n' "$FILESYSTEM_TOTAL_INODES"
printf 'filesystem_free_inodes=%s\n' "$FILESYSTEM_FREE_INODES"

if ! MOUNT_FSTYPE=$(
    timeout --signal=TERM --kill-after=5s 15s \
        findmnt -rn --raw -T "$STAGING_PARENT" -o FSTYPE 2>/dev/null
); then
    fail_not_determinable 20 'staging_filesystem_type_unavailable'
fi

if ! MOUNT_OPTIONS=$(
    timeout --signal=TERM --kill-after=5s 15s \
        findmnt -rn --raw -T "$STAGING_PARENT" -o OPTIONS 2>/dev/null
); then
    fail_not_determinable 20 'staging_mount_options_unavailable'
fi

check_single_line "$MOUNT_FSTYPE" 'staging_filesystem_type'
check_single_line "$MOUNT_OPTIONS" 'staging_mount_options'

printf 'staging_filesystem_type=%s\n' "$MOUNT_FSTYPE"

printf '%s\n' 'section=size'

if ! ALLOCATED_BYTES=$(
    timeout --signal=TERM --kill-after=10s 180s \
        bash -o pipefail -c '
            du -sx --block-size=1 -- "$1" 2>/dev/null |
                awk "$2"
        ' bash "$CHROMA" "$DU_AWK" 2>/dev/null
); then
    fail_not_determinable 40 'allocated_size_timeout_error_or_invalid'
fi

normalize_or_fail \
    ALLOCATED_BYTES \
    "$ALLOCATED_BYTES" \
    'allocated_size_invalid'

printf 'allocated_bytes=%s\n' "$ALLOCATED_BYTES"

if ! APPARENT_BYTES=$(
    timeout --signal=TERM --kill-after=10s 180s \
        bash -o pipefail -c '
            du -sx --apparent-size --block-size=1 \
                -- "$1" 2>/dev/null |
                awk "$2"
        ' bash "$CHROMA" "$DU_AWK" 2>/dev/null
); then
    fail_not_determinable 40 'apparent_size_timeout_error_or_invalid'
fi

normalize_or_fail \
    APPARENT_BYTES \
    "$APPARENT_BYTES" \
    'apparent_size_invalid'

printf 'apparent_bytes=%s\n' "$APPARENT_BYTES"

printf '%s\n' 'section=structure'

if ! STRUCTURE_OUTPUT=$(
    timeout --signal=TERM --kill-after=10s 180s \
        bash -o pipefail -c '
            find -P "$1" -xdev \
                -printf "%y\t%D\t%i\t%n\n" 2>/dev/null |
                awk -F "\t" "$2" |
                sort
        ' bash "$CHROMA" "$STRUCTURE_AWK" 2>/dev/null
); then
    fail_not_determinable \
        50 \
        'structural_scan_timeout_access_error_or_invalid'
fi

if ! STRUCTURE_VALUES=$(
    printf '%s\n' "$STRUCTURE_OUTPUT" |
        awk "$STRUCTURE_VALIDATE_AWK"
); then
    fail_not_determinable \
        50 \
        'structural_metrics_missing_duplicate_or_malformed'
fi

mapfile -t STRUCTURE_VALUE_ARRAY <<< "$STRUCTURE_VALUES"

if [ "${#STRUCTURE_VALUE_ARRAY[@]}" -ne 12 ]; then
    fail_not_determinable \
        50 \
        'structural_metric_cardinality_invalid'
fi

normalize_or_fail \
    OBJECT_COUNT \
    "${STRUCTURE_VALUE_ARRAY[0]}" \
    'object_count_invalid'

normalize_or_fail \
    REGULAR_FILE_COUNT \
    "${STRUCTURE_VALUE_ARRAY[1]}" \
    'regular_file_count_invalid'

normalize_or_fail \
    DIRECTORY_COUNT \
    "${STRUCTURE_VALUE_ARRAY[2]}" \
    'directory_count_invalid'

normalize_or_fail \
    SYMLINK_COUNT \
    "${STRUCTURE_VALUE_ARRAY[3]}" \
    'symlink_count_invalid'

normalize_or_fail \
    BLOCK_DEVICE_COUNT \
    "${STRUCTURE_VALUE_ARRAY[4]}" \
    'block_device_count_invalid'

normalize_or_fail \
    CHAR_DEVICE_COUNT \
    "${STRUCTURE_VALUE_ARRAY[5]}" \
    'char_device_count_invalid'

normalize_or_fail \
    FIFO_COUNT \
    "${STRUCTURE_VALUE_ARRAY[6]}" \
    'fifo_count_invalid'

normalize_or_fail \
    SOCKET_COUNT \
    "${STRUCTURE_VALUE_ARRAY[7]}" \
    'socket_count_invalid'

normalize_or_fail \
    DOOR_COUNT \
    "${STRUCTURE_VALUE_ARRAY[8]}" \
    'door_count_invalid'

normalize_or_fail \
    HARDLINK_INTERNAL_COUNT \
    "${STRUCTURE_VALUE_ARRAY[9]}" \
    'hardlink_internal_count_invalid'

normalize_or_fail \
    HARDLINK_EXTERNAL_COUNT \
    "${STRUCTURE_VALUE_ARRAY[10]}" \
    'hardlink_external_count_invalid'

normalize_or_fail \
    HARDLINK_INCONSISTENT_COUNT \
    "${STRUCTURE_VALUE_ARRAY[11]}" \
    'hardlink_inconsistent_count_invalid'

STRUCTURE_TYPE_SUM='0'

safe_structure_add_or_fail \
    STRUCTURE_TYPE_SUM \
    "$STRUCTURE_TYPE_SUM" \
    "$REGULAR_FILE_COUNT" \
    'structure_type_sum_regular_overflow'

safe_structure_add_or_fail \
    STRUCTURE_TYPE_SUM \
    "$STRUCTURE_TYPE_SUM" \
    "$DIRECTORY_COUNT" \
    'structure_type_sum_directory_overflow'

safe_structure_add_or_fail \
    STRUCTURE_TYPE_SUM \
    "$STRUCTURE_TYPE_SUM" \
    "$SYMLINK_COUNT" \
    'structure_type_sum_symlink_overflow'

safe_structure_add_or_fail \
    STRUCTURE_TYPE_SUM \
    "$STRUCTURE_TYPE_SUM" \
    "$BLOCK_DEVICE_COUNT" \
    'structure_type_sum_block_overflow'

safe_structure_add_or_fail \
    STRUCTURE_TYPE_SUM \
    "$STRUCTURE_TYPE_SUM" \
    "$CHAR_DEVICE_COUNT" \
    'structure_type_sum_char_overflow'

safe_structure_add_or_fail \
    STRUCTURE_TYPE_SUM \
    "$STRUCTURE_TYPE_SUM" \
    "$FIFO_COUNT" \
    'structure_type_sum_fifo_overflow'

safe_structure_add_or_fail \
    STRUCTURE_TYPE_SUM \
    "$STRUCTURE_TYPE_SUM" \
    "$SOCKET_COUNT" \
    'structure_type_sum_socket_overflow'

safe_structure_add_or_fail \
    STRUCTURE_TYPE_SUM \
    "$STRUCTURE_TYPE_SUM" \
    "$DOOR_COUNT" \
    'structure_type_sum_door_overflow'

if [ "$STRUCTURE_TYPE_SUM" != "$OBJECT_COUNT" ]; then
    fail_not_determinable \
        50 \
        'structure_type_sum_mismatch'
fi

safe_add_or_fail \
    SPECIAL_FILE_COUNT \
    "$BLOCK_DEVICE_COUNT" \
    "$CHAR_DEVICE_COUNT" \
    'special_file_block_char_overflow'

safe_add_or_fail \
    SPECIAL_FILE_COUNT \
    "$SPECIAL_FILE_COUNT" \
    "$FIFO_COUNT" \
    'special_file_fifo_overflow'

safe_add_or_fail \
    SPECIAL_FILE_COUNT \
    "$SPECIAL_FILE_COUNT" \
    "$SOCKET_COUNT" \
    'special_file_socket_overflow'

safe_add_or_fail \
    SPECIAL_FILE_COUNT \
    "$SPECIAL_FILE_COUNT" \
    "$DOOR_COUNT" \
    'special_file_door_overflow'

printf 'object_count=%s\n' "$OBJECT_COUNT"
printf 'regular_file_count=%s\n' "$REGULAR_FILE_COUNT"
printf 'directory_count=%s\n' "$DIRECTORY_COUNT"
printf 'symlink_count=%s\n' "$SYMLINK_COUNT"
printf 'special_file_count=%s\n' "$SPECIAL_FILE_COUNT"
printf 'hardlink_internal_complete=%s\n' "$HARDLINK_INTERNAL_COUNT"
printf 'hardlink_external_not_resolved=%s\n' "$HARDLINK_EXTERNAL_COUNT"
printf 'hardlink_inconsistent=%s\n' "$HARDLINK_INCONSISTENT_COUNT"

printf '%s\n' 'section=quota'

QUOTA_STATE='NOT_OBSERVED_NOT_PROVEN_ABSENT'
USER_QUOTA_STATE='NOT_OBSERVED_NOT_PROVEN_ABSENT'
GROUP_QUOTA_STATE='NOT_OBSERVED_NOT_PROVEN_ABSENT'
PROJECT_QUOTA_STATE='NOT_OBSERVED_NOT_PROVEN_ABSENT'

case ",$MOUNT_OPTIONS," in
    *,usrquota,*|*,uquota,*|*,quota,*)
        if command -v quota >/dev/null 2>&1; then
            if timeout --signal=TERM --kill-after=5s 15s \
                quota -s -w -v -u "$(id -un)" \
                >/dev/null 2>&1
            then
                USER_QUOTA_STATE='OBSERVED_NOT_NORMALIZED'
            else
                USER_QUOTA_STATE='PRIVILEGED_CHECK_REQUIRED'
            fi
        else
            USER_QUOTA_STATE='PRIVILEGED_CHECK_REQUIRED'
        fi
        ;;
esac

case ",$MOUNT_OPTIONS," in
    *,grpquota,*|*,gquota,*)
        if command -v quota >/dev/null 2>&1; then
            if timeout --signal=TERM --kill-after=5s 15s \
                quota -s -w -v -g "$(id -gn)" \
                >/dev/null 2>&1
            then
                GROUP_QUOTA_STATE='OBSERVED_NOT_NORMALIZED'
            else
                GROUP_QUOTA_STATE='PRIVILEGED_CHECK_REQUIRED'
            fi
        else
            GROUP_QUOTA_STATE='PRIVILEGED_CHECK_REQUIRED'
        fi
        ;;
esac

case ",$MOUNT_OPTIONS," in
    *,prjquota,*|*,pquota,*)
        PROJECT_QUOTA_STATE='PRIVILEGED_CHECK_REQUIRED'
        ;;
esac

if [ "$USER_QUOTA_STATE" = 'PRIVILEGED_CHECK_REQUIRED' ] ||
   [ "$GROUP_QUOTA_STATE" = 'PRIVILEGED_CHECK_REQUIRED' ] ||
   [ "$PROJECT_QUOTA_STATE" = 'PRIVILEGED_CHECK_REQUIRED' ]; then
    QUOTA_STATE='PRIVILEGED_CHECK_REQUIRED'
elif [ "$USER_QUOTA_STATE" = 'OBSERVED_NOT_NORMALIZED' ] ||
     [ "$GROUP_QUOTA_STATE" = 'OBSERVED_NOT_NORMALIZED' ] ||
     [ "$PROJECT_QUOTA_STATE" = 'OBSERVED_NOT_NORMALIZED' ]; then
    QUOTA_STATE='OBSERVED_NOT_NORMALIZED'
else
    QUOTA_STATE='NOT_OBSERVED_NOT_PROVEN_ABSENT'
fi

printf 'user_quota_state=%s\n' "$USER_QUOTA_STATE"
printf 'group_quota_state=%s\n' "$GROUP_QUOTA_STATE"
printf 'project_quota_state=%s\n' "$PROJECT_QUOTA_STATE"
printf 'quota_state=%s\n' "$QUOTA_STATE"

printf '%s\n' 'section=capacity_model'

max_uint64_or_fail \
    COPY_BASIS_BYTES \
    "$ALLOCATED_BYTES" \
    "$APPARENT_BYTES" \
    'copy_basis_invalid'

safe_percent_or_fail \
    MANIFEST_OVERHEAD_BYTES \
    "$COPY_BASIS_BYTES" \
    5 \
    'manifest_overhead_overflow'

max_uint64_or_fail \
    MANIFEST_OVERHEAD_BYTES \
    "$MANIFEST_OVERHEAD_BYTES" \
    "$GIB" \
    'manifest_overhead_minimum_invalid'

safe_percent_or_fail \
    GROWTH_MARGIN_BYTES \
    "$COPY_BASIS_BYTES" \
    20 \
    'growth_margin_overflow'

max_uint64_or_fail \
    GROWTH_MARGIN_BYTES \
    "$GROWTH_MARGIN_BYTES" \
    "$GIB" \
    'growth_margin_minimum_invalid'

safe_percent_or_fail \
    OPERATIONAL_RESERVE_BYTES \
    "$FILESYSTEM_TOTAL_BYTES" \
    10 \
    'operational_reserve_overflow'

safe_add_or_fail \
    TWO_GIB \
    "$GIB" \
    "$GIB" \
    'two_gib_overflow'

safe_add_or_fail \
    THREE_GIB \
    "$TWO_GIB" \
    "$GIB" \
    'three_gib_overflow'

safe_add_or_fail \
    FOUR_GIB \
    "$THREE_GIB" \
    "$GIB" \
    'four_gib_overflow'

safe_add_or_fail \
    FIVE_GIB \
    "$FOUR_GIB" \
    "$GIB" \
    'five_gib_overflow'

max_uint64_or_fail \
    OPERATIONAL_RESERVE_BYTES \
    "$OPERATIONAL_RESERVE_BYTES" \
    "$FIVE_GIB" \
    'operational_reserve_minimum_invalid'

safe_add_or_fail \
    REQUIRED_BYTES \
    "$COPY_BASIS_BYTES" \
    "$MANIFEST_OVERHEAD_BYTES" \
    'required_bytes_manifest_overflow'

safe_add_or_fail \
    REQUIRED_BYTES \
    "$REQUIRED_BYTES" \
    "$GROWTH_MARGIN_BYTES" \
    'required_bytes_growth_overflow'

safe_add_or_fail \
    REQUIRED_BYTES \
    "$REQUIRED_BYTES" \
    "$OPERATIONAL_RESERVE_BYTES" \
    'required_bytes_operational_reserve_overflow'

safe_percent_or_fail \
    INODE_RESERVE \
    "$OBJECT_COUNT" \
    10 \
    'inode_reserve_overflow'

max_uint64_or_fail \
    INODE_RESERVE \
    "$INODE_RESERVE" \
    "$MINIMUM_INODE_RESERVE" \
    'inode_reserve_minimum_invalid'

safe_add_or_fail \
    REQUIRED_FREE_INODES \
    "$OBJECT_COUNT" \
    "$INODE_RESERVE" \
    'required_free_inodes_overflow'

printf 'copy_basis_bytes=%s\n' "$COPY_BASIS_BYTES"
printf 'manifest_overhead_bytes=%s\n' "$MANIFEST_OVERHEAD_BYTES"
printf 'growth_margin_bytes=%s\n' "$GROWTH_MARGIN_BYTES"
printf 'operational_reserve_bytes=%s\n' "$OPERATIONAL_RESERVE_BYTES"
printf 'required_bytes=%s\n' "$REQUIRED_BYTES"
printf 'inode_reserve=%s\n' "$INODE_RESERVE"
printf 'required_free_inodes=%s\n' "$REQUIRED_FREE_INODES"

CAPACITY_BLOCK=0
STRUCTURE_BLOCK=0

if [ "$FILESYSTEM_AVAILABLE_BYTES" -lt "$REQUIRED_BYTES" ]; then
    CAPACITY_BLOCK=1
fi

if [ "$FILESYSTEM_FREE_INODES" -lt "$REQUIRED_FREE_INODES" ]; then
    CAPACITY_BLOCK=1
fi

if [ "$STAGING_ACCESS_BLOCK" -ne 0 ]; then
    CAPACITY_BLOCK=1
fi

if [ "$SYMLINK_COUNT" -ne 0 ] ||
   [ "$SPECIAL_FILE_COUNT" -ne 0 ] ||
   [ "$HARDLINK_EXTERNAL_COUNT" -ne 0 ] ||
   [ "$HARDLINK_INCONSISTENT_COUNT" -ne 0 ]; then
    STRUCTURE_BLOCK=1
fi

if [ "$CAPACITY_BLOCK" -eq 0 ]; then
    CAPACITY_ASSESSMENT='sufficient_within_observed_limits'
else
    CAPACITY_ASSESSMENT='insufficient_or_staging_access_blocked'
fi

if [ "$STRUCTURE_BLOCK" -eq 0 ]; then
    STRUCTURE_ASSESSMENT='no_observed_structure_block'
else
    STRUCTURE_ASSESSMENT='observed_structure_block'
fi

printf 'capacity_block=%s\n' "$CAPACITY_BLOCK"
printf 'capacity_assessment=%s\n' "$CAPACITY_ASSESSMENT"
printf 'structure_block=%s\n' "$STRUCTURE_BLOCK"
printf 'structure_assessment=%s\n' "$STRUCTURE_ASSESSMENT"

printf '%s\n' 'section=post_scan_identity'

if ! CHROMA_ID_AFTER=$(
    stat -c '%d:%i:%Z:%Y' -- "$CHROMA" 2>/dev/null
); then
    fail_not_determinable 20 'chroma_final_stat_failed'
fi

if ! STAGING_ID_AFTER=$(
    stat -c '%d:%i:%Z:%Y' -- "$STAGING_PARENT" 2>/dev/null
); then
    fail_not_determinable 20 'staging_final_stat_failed'
fi

if [ "$CHROMA_ID_BEFORE" = "$CHROMA_ID_AFTER" ]; then
    printf '%s\n' 'chroma_root_metadata_stable=yes'
else
    printf '%s\n' 'chroma_root_metadata_stable=no'
    fail_not_determinable 20 'chroma_root_metadata_changed'
fi

if [ "$STAGING_ID_BEFORE" = "$STAGING_ID_AFTER" ]; then
    printf '%s\n' 'staging_root_metadata_stable=yes'
else
    printf '%s\n' 'staging_root_metadata_stable=no'
    fail_not_determinable 20 'staging_root_metadata_changed'
fi

if [ "$QUOTA_STATE" != 'VERIFIED' ]; then
    finish_result \
        2 \
        "INCOMPLETE|reason=quota_${QUOTA_STATE}"
fi

if [ "$CAPACITY_BLOCK" -ne 0 ] ||
   [ "$STRUCTURE_BLOCK" -ne 0 ]; then
    finish_result 3 'COMPLETE_CAPACITY_FAIL'
fi

finish_result 0 'COMPLETE_CAPACITY_PASS'
