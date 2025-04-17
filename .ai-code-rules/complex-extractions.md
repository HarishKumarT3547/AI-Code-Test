# Complex Extractions in Clauses

This rule checks for complex extractions in pattern matching clauses.

```pattern
Complex Extraction
r'case\s+\w+\s+do\s+.*?->\s*{.*?}.*?end'
Complex extraction in case statement. Consider breaking down the pattern matching into smaller, more manageable pieces.
Instead of:
case user do
  %User{name: name, age: age, address: %Address{street: street}} -> {name, age, street}
end

Try:
case user do
  %User{name: name, age: age, address: address} ->
    %Address{street: street} = address
    {name, age, street}
end
```

```pattern
Nested Pattern Matching
r'%\{.*?%\{.*?\}.*?\}'
Nested pattern matching in a single line. Consider extracting nested structures into separate pattern matches.
Instead of:
%User{address: %Address{street: street}} = user

Try:
%User{address: address} = user
%Address{street: street} = address
```
