%% @doc This module demonstrates various Erlang code rules and best practices.
%% It includes examples of both good and bad practices to illustrate the rules.
-module(code_rules_example).

%% API exports
-export([
    process_data/1,
    calculate_total/2,
    validate_input/1,
    handle_request/2,
    transform_data/1,
    bad_example/3
]).

%% Types
-type status() :: success | error.
-type result() :: {status(), term()}.
-type user_data() :: #{name => string(), age => integer(), email => string()}.

%% @doc Processes user data with proper error handling and validation.
-spec process_data(user_data()) -> result().
process_data(Data) ->
    try
        validate_input(Data),
        Transformed = transform_data(Data),
        {success, Transformed}
    catch
        error:Reason ->
            {error, {invalid_data, Reason}}
    end.

%% @doc Calculates total with proper type checking and error handling.
-spec calculate_total(number(), number()) -> number().
calculate_total(Price, Quantity) when is_number(Price), is_number(Quantity) ->
    Price * Quantity;
calculate_total(_, _) ->
    error(badarg).

%% @doc Validates input data with proper pattern matching.
-spec validate_input(user_data()) -> ok | no_return().
validate_input(#{name := Name, age := Age, email := Email}) ->
    case {is_valid_name(Name), is_valid_age(Age), is_valid_email(Email)} of
        {true, true, true} -> ok;
        _ -> error(invalid_data)
    end.

%% @doc Handles HTTP request with proper error handling and logging.
-spec handle_request(atom(), map()) -> {ok, term()} | {error, term()}.
handle_request(Method, Request) ->
    try
        case Method of
            get -> handle_get(Request);
            post -> handle_post(Request);
            _ -> {error, unsupported_method}
        end
    catch
        error:Reason ->
            error_logger:error_msg("Request failed: ~p", [Reason]),
            {error, Reason}
    end.

%% @doc Transforms data with proper pattern matching and guards.
-spec transform_data(user_data()) -> user_data().
transform_data(#{name := Name, age := Age} = Data) ->
    Data#{name => string:to_upper(Name), age => Age + 1}.

%% @doc Example of bad practices to avoid.
-spec bad_example(term(), term(), term()) -> term().
bad_example(Arg1, Arg2, Arg3) ->
    %% Bad: No type checking
    Result = case Arg1 of
        _ when is_integer(Arg1) -> Arg1 + Arg2;
        _ -> Arg3
    end,
    %% Bad: Magic numbers
    if
        Result > 100 -> Result * 2;
        true -> Result * 3
    end.

%% Private functions
-spec is_valid_name(string()) -> boolean().
is_valid_name(Name) ->
    length(Name) > 0 andalso length(Name) =< 100.

-spec is_valid_age(integer()) -> boolean().
is_valid_age(Age) ->
    Age >= 0 andalso Age =< 150.

-spec is_valid_email(string()) -> boolean().
is_valid_email(Email) ->
    re:run(Email, "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$") =/= nomatch.

-spec handle_get(map()) -> {ok, term()} | {error, term()}.
handle_get(Request) ->
    case maps:get(id, Request, undefined) of
        undefined -> {error, missing_id};
        Id -> {ok, {id, Id}}
    end.

-spec handle_post(map()) -> {ok, term()} | {error, term()}.
handle_post(Request) ->
    case maps:get(data, Request, undefined) of
        undefined -> {error, missing_data};
        Data -> {ok, Data}
    end.

%% @doc Example of proper test cases
-ifdef(TEST).
-include_lib("eunit/include/eunit.hrl").

process_data_test() ->
    ?assertEqual(
        {success, #{name => "JOHN", age => 31, email => "test@example.com"}},
        process_data(#{name => "John", age => 30, email => "test@example.com"})
    ),
    ?assertEqual(
        {error, {invalid_data, invalid_data}},
        process_data(#{name => "", age => 30, email => "test@example.com"})
    ).

calculate_total_test() ->
    ?assertEqual(100, calculate_total(10, 10)),
    ?assertError(badarg, calculate_total(10, "invalid")).

validate_input_test() ->
    ?assertEqual(ok, validate_input(#{name => "John", age => 30, email => "test@example.com"})),
    ?assertError(invalid_data, validate_input(#{name => "", age => 30, email => "test@example.com"})).

-endif. 