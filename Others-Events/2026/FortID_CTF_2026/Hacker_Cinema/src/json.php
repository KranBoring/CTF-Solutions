<?php
function canonicalize_value(mixed $value): mixed {
    if (is_array($value)) {
        $isList = array_keys($value) === range(0, count($value) - 1);
        if ($isList) {
            return array_map('canonicalize_value', $value);
        }
        ksort($value, SORT_STRING);
        foreach ($value as $k => $v) {
            $value[$k] = canonicalize_value($v);
        }
    }
    return $value;
}

function canonical_json(mixed $value): string {
    return json_encode(
        canonicalize_value($value),
        JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_PRESERVE_ZERO_FRACTION
    );
}
