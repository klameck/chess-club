## Assignment 3 - Perft Test 
Trial from 06.11.2026

```python -m ccc26.eval.perft --board ccc26.board.MyBoard --depth 4 --mode compare --fen "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"```
### Standart Position

[BitBoard ] Nodes: 20 | Time: 0.0143s
[BitBoard ] Nodes: 400 | Time: 0.3625s
[BitBoard ] Nodes: 8,902 | Time: 8.1126s
[BitBoard ] Nodes: 197,281 | Time: 263.5625s

Starting Perft Test (Mode: compare, Divide: False)
Board Class: MyBoard
FEN: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1


### Kiwi-Pete Position

[BitBoard ] Nodes: 48 | Time: 0.0868s
[BitBoard ] Nodes: 2,039 | Time: 4.1374s
[BitBoard ] Nodes: 97,862 | Time: 193.4351s

Starting Perft Test (Mode: custom, Divide: False)
Board Class: MyBoard
FEN: r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1

### En Passant/ Pins Position

[BitBoard ] Nodes: 14 | Time: 0.0130s
[BitBoard ] Nodes: 191 | Time: 0.2049s
[BitBoard ] Nodes: 2,812 | Time: 2.7980s

Starting Perft Test (Mode: custom, Divide: False)
Board Class: MyBoard
FEN: 8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1

## Assignment 3 - Flamegraph
run in terminal: 
```py-spy record --rate 1000 --format speedscope -o bitboard-profile.json -- python -m ccc26.eval.perft --board ccc26.board.Bitboard -d 3 --mode custom```

open created json file in the app: https://www.speedscope.app/ 

or 

create a flamegraph svg file by running this code:
```py-spy record --rate 1000 --format flamegraph -o bitboard-flamegraph.svg -- python -m ccc26.eval.perft --board ccc26.board.Bitboard -d 3 --mode custom```

## Assignment 3 - Profiling 

Trial from 06.11.2026
```
Starting Perft Test (Mode: custom, Divide: False)
Board Class: MyBoard
FEN: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
------------------------------------------------------------

--- Depth 1 ---
[MyBoard  ] Nodes: 20 | Time: 0.0087s

--- Depth 2 ---
[MyBoard  ] Nodes: 400 | Time: 0.1939s

--- Depth 3 ---
[MyBoard  ] Nodes: 8,902 | Time: 4.7372s
         6257300 function calls (6247318 primitive calls) in 5.173 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     24/1    0.002    0.000    5.173    5.173 {built-in method builtins.exec}
        1    0.000    0.000    5.173    5.173 <frozen runpy>:201(run_module)
        1    0.000    0.000    5.170    5.170 <frozen runpy>:65(_run_code)
        1    0.000    0.000    5.170    5.170 perft.py:1(<module>)
        1    0.000    0.000    4.960    4.960 perft.py:262(main)
        1    0.000    0.000    4.942    4.942 perft.py:166(run_perft_session)
   9765/3    0.019    0.000    4.940    1.647 perft.py:81(custom_perft)
     9762    0.094    0.000    4.645    0.000 board.py:663(push_move)
    10205    1.314    0.000    4.416    0.000 board.py:432(get_legal_moves)
   229742    1.041    0.000    1.041    0.000 board.py:575(square_attacked)
   229742    0.180    0.000    0.688    0.000 board.py:369(convert_to_uci)
   498532    0.452    0.000    0.568    0.000 board.py:569(_from_uci)
   459484    0.387    0.000    0.508    0.000 board.py:364(coord)
     9763    0.254    0.000    0.278    0.000 board.py:274(to_fen)
    40820    0.149    0.000    0.273    0.000 board.py:452(diagonal_moves)
  1061959    0.246    0.000    0.246    0.000 {method 'append' of 'list' objects}
     19/6    0.000    0.000    0.226    0.038 <frozen importlib._bootstrap>:1349(_find_and_load)
     18/5    0.000    0.000    0.225    0.045 <frozen importlib._bootstrap>:1304(_find_and_load_unlocked)
     17/6    0.000    0.000    0.222    0.037 <frozen importlib._bootstrap>:911(_load_unlocked)
     11/5    0.000    0.000    0.222    0.044 <frozen importlib._bootstrap_external>:993(exec_module)
    38/11    0.000    0.000    0.218    0.020 <frozen importlib._bootstrap>:480(_call_with_frames_removed)
        3    0.000    0.000    0.204    0.068 __init__.py:1(<module>)
   479963    0.196    0.000    0.196    0.000 {method 'remove' of 'list' objects}
    40820    0.122    0.000    0.190    0.000 board.py:440(straight_moves)
        3    0.007    0.002    0.184    0.061 __init__.py:534(_attack_table)
    10816    0.035    0.000    0.177    0.000 __init__.py:495(_sliding_attacks)
  1456601    0.174    0.000    0.174    0.000 {built-in method builtins.ord}
   681702    0.167    0.000    0.167    0.000 board.py:345(steppable)
    53810    0.085    0.000    0.142    0.000 __init__.py:266(square_distance)
     9762    0.045    0.000    0.088    0.000 board.py:757(pop_move)
   459484    0.063    0.000    0.063    0.000 {built-in method builtins.chr}
    53845    0.017    0.000    0.017    0.000 {built-in method builtins.max}
        6    0.000    0.000    0.016    0.003 argparse.py:1451(add_argument)
        1    0.000    0.000    0.016    0.016 argparse.py:1772(__init__)
   114234    0.015    0.000    0.015    0.000 {built-in method builtins.abs}
        6    0.000    0.000    0.015    0.003 argparse.py:2607(_get_formatter)
        6    0.000    0.000    0.015    0.003 argparse.py:164(__init__)
   107812    0.014    0.000    0.014    0.000 __init__.py:262(square_rank)
   107812    0.013    0.000    0.013    0.000 __init__.py:258(square_file)
        1    0.000    0.000    0.012    0.012 shutil.py:1(<module>)
    39069    0.010    0.000    0.010    0.000 {method 'pop' of 'list' objects}
       12    0.000    0.000    0.009    0.001 <frozen importlib._bootstrap_external>:1066(get_code)
    10205    0.008    0.000    0.008    0.000 board.py:372(do_castling)
       19    0.000    0.000    0.008    0.000 <frozen importlib._bootstrap>:1240(_find_spec)
30817/30785    0.008    0.000    0.008    0.000 {built-in method builtins.len}
       16    0.000    0.000    0.007    0.000 <frozen importlib._bootstrap_external>:1524(find_spec)
       16    0.000    0.000    0.007    0.000 <frozen importlib._bootstrap_external>:1495(_get_spec)
       40    0.001    0.000    0.006    0.000 <frozen importlib._bootstrap_external>:1597(find_spec)
    10036    0.006    0.000    0.006    0.000 {method 'join' of 'str' objects}
       17    0.000    0.000    0.006    0.000 <frozen importlib._bootstrap>:806(module_from_spec)
        2    0.000    0.000    0.005    0.003 <frozen importlib._bootstrap_external>:1291(create_module)
        2    0.005    0.003    0.005    0.003 {built-in method _imp.create_dynamic}
      256    0.000    0.000    0.005    0.000 __init__.py:513(_step_attacks)
       12    0.000    0.000    0.005    0.000 <frozen importlib._bootstrap_external>:755(_compile_bytecode)
        1    0.000    0.000    0.004    0.004 bz2.py:1(<module>)
       12    0.004    0.000    0.004    0.000 {built-in method marshal.loads}
     9762    0.004    0.000    0.004    0.000 {method 'copy' of 'dict' objects}
        3    0.000    0.000    0.004    0.001 dataclasses.py:1264(wrap)
        3    0.000    0.000    0.004    0.001 dataclasses.py:921(_process_class)
    10560    0.003    0.000    0.003    0.000 __init__.py:525(_carry_rippler)
        1    0.003    0.003    0.003    0.003 __init__.py:555(_rays)
       12    0.000    0.000    0.003    0.000 <frozen importlib._bootstrap_external>:1187(get_data)
    58/56    0.001    0.000    0.003    0.000 {built-in method builtins.__build_class__}
        1    0.000    0.000    0.003    0.003 <frozen runpy>:105(_get_module_details)
      203    0.002    0.000    0.003    0.000 <frozen importlib._bootstrap_external>:96(_path_join)
        1    0.000    0.000    0.003    0.003 lzma.py:1(<module>)
        3    0.000    0.000    0.003    0.001 dataclasses.py:1247(dataclass)
       20    0.000    0.000    0.003    0.000 __init__.py:280(_compile)
       84    0.000    0.000    0.002    0.000 <frozen importlib._bootstrap_external>:140(_path_stat)
       17    0.000    0.000    0.002    0.000 __init__.py:226(compile)
       84    0.002    0.000    0.002    0.000 {built-in method nt.stat}
       10    0.000    0.000    0.002    0.000 dataclasses.py:449(_create_fn)
        6    0.000    0.000    0.002    0.000 _compiler.py:745(compile)
      3/2    0.000    0.000    0.002    0.001 {built-in method builtins.__import__}
        1    0.000    0.000    0.002    0.002 argparse.py:1903(parse_args)
        1    0.000    0.000    0.002    0.002 argparse.py:1913(parse_known_args)
        1    0.000    0.000    0.002    0.002 argparse.py:1916(_parse_known_args2)
        1    0.001    0.001    0.002    0.002 argparse.py:1954(_parse_known_args)
       12    0.002    0.000    0.002    0.000 {built-in method _io.open_code}
       12    0.001    0.000    0.001    0.000 {method 'read' of '_io.BufferedReader' objects}
        6    0.000    0.000    0.001    0.000 _parser.py:969(parse)
     13/6    0.000    0.000    0.001    0.000 _parser.py:452(_parse_sub)
       10    0.001    0.000    0.001    0.000 {built-in method builtins.print}
     15/7    0.000    0.000    0.001    0.000 _parser.py:512(_parse)
        2    0.000    0.000    0.001    0.001 enum.py:528(__new__)
    56/28    0.000    0.000    0.001    0.000 {built-in method __new__ of type object at 0x00007FFAA42257D0}
        3    0.000    0.000    0.001    0.000 dataclasses.py:568(_init_fn)
       29    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:150(_path_is_mode_type)
        6    0.000    0.000    0.001    0.000 _compiler.py:578(_code)
       18    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap>:416(__enter__)
       25    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:159(_path_isfile)
        3    0.000    0.000    0.001    0.000 dataclasses.py:661(_cmp_fn)
       28    0.000    0.000    0.001    0.000 enum.py:254(__set_name__)
       24    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:486(cache_from_source)
        1    0.000    0.000    0.001    0.001 fnmatch.py:1(<module>)
     30/6    0.000    0.000    0.001    0.000 _compiler.py:37(_compile)
        3    0.000    0.000    0.001    0.000 dataclasses.py:627(_repr_fn)
       17    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap>:733(_init_module_attrs)
        1    0.000    0.000    0.001    0.001 argparse.py:1(<module>)
        3    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:1648(_fill_cache)
        1    0.000    0.000    0.001    0.001 <frozen importlib._bootstrap>:1171(exec_module)
        1    0.000    0.000    0.001    0.001 <frozen posixpath>:1(<module>)
       18    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap>:304(acquire)
       25    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:632(cached)
        3    0.000    0.000    0.000    0.000 {built-in method nt.listdir}
       35    0.000    0.000    0.000    0.000 enum.py:390(__setitem__)
        1    0.000    0.000    0.000    0.000 <frozen importlib.util>:70(find_spec)
        6    0.000    0.000    0.000    0.000 shutil.py:1404(get_terminal_size)
       14    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:615(_get_cached)
        3    0.000    0.000    0.000    0.000 argparse.py:1369(__init__)
        1    0.000    0.000    0.000    0.000 board.py:137(__init__)
        6    0.000    0.000    0.000    0.000 typing.py:392(inner)
      192    0.000    0.000    0.000    0.000 __init__.py:521(_edges)
       51    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1473(_path_importer_cache)
      634    0.000    0.000    0.000    0.000 {method 'rstrip' of 'str' objects}
       18    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:426(_get_module_lock)
      522    0.000    0.000    0.000    0.000 {method 'startswith' of 'str' objects}
        6    0.000    0.000    0.000    0.000 {built-in method nt.get_terminal_size}
        3    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1460(_path_hooks)
       12    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1206(path_stats)
        1    0.000    0.000    0.000    0.000 board.py:208(load_fen)
      714    0.000    0.000    0.000    0.000 {method 'endswith' of 'str' objects}
        7    0.000    0.000    0.000    0.000 <frozen abc>:105(__new__)
        1    0.000    0.000    0.000    0.000 __init__.py:118(Termination)
       12    0.000    0.000    0.000    0.000 {method '__exit__' of '_io._IOBase' objects}
        3    0.000    0.000    0.000    0.000 gettext.py:616(gettext)
        1    0.000    0.000    0.000    0.000 __init__.py:355(namedtuple)
        3    0.000    0.000    0.000    0.000 gettext.py:578(dgettext)
        3    0.000    0.000    0.000    0.000 argparse.py:2021(consume_optional)
       14    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1592(_get_spec)
        8    0.000    0.000    0.000    0.000 dataclasses.py:760(_get_field)
        1    0.000    0.000    0.000    0.000 __init__.py:78(Status)
        3    0.000    0.000    0.000    0.000 gettext.py:519(translation)
       18    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:162(__enter__)
      840    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
       14    0.000    0.000    0.000    0.000 _compiler.py:243(_optimize_charset)
        3    0.000    0.000    0.000    0.000 dataclasses.py:372(__init__)
       24    0.000    0.000    0.000    0.000 dataclasses.py:701(_is_type)
        3    0.000    0.000    0.000    0.000 gettext.py:479(find)
        1    0.000    0.000    0.000    0.000 board.py:1(<module>)
        5    0.000    0.000    0.000    0.000 typing.py:1269(__init__)
       14    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:806(spec_from_file_location)
        6    0.000    0.000    0.000    0.000 _compiler.py:516(_compile_info)
       24    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:132(_path_split)
       18    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:124(setdefault)
       24    0.000    0.000    0.000    0.000 <frozen os>:709(__getitem__)
        3    0.000    0.000    0.000    0.000 argparse.py:2281(_match_argument)
      178    0.000    0.000    0.000    0.000 _parser.py:168(__getitem__)
        3    0.000    0.000    0.000    0.000 __init__.py:164(match)
        2    0.000    0.000    0.000    0.000 typing.py:521(__getitem__)
       90    0.000    0.000    0.000    0.000 {built-in method builtins.setattr}
       91    0.000    0.000    0.000    0.000 enum.py:849(__setattr__)
       19    0.000    0.000    0.000    0.000 __init__.py:101(find_spec)
        1    0.000    0.000    0.000    0.000 dataclasses.py:882(_hash_add)
       12    0.000    0.000    0.000    0.000 enum.py:1561(__and__)
        1    0.000    0.000    0.000    0.000 {built-in method builtins.eval}
        3    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1689(path_hook_for_FileFinder)
        2    0.000    0.000    0.000    0.000 typing.py:753(Literal)
        6    0.000    0.000    0.000    0.000 typing.py:175(_type_check)
        1    0.000    0.000    0.000    0.000 dataclasses.py:675(_hash_fn)
      116    0.000    0.000    0.000    0.000 _parser.py:261(get)
       12    0.000    0.000    0.000    0.000 <frozen _collections_abc>:804(get)
       18    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:420(__exit__)
       17    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:185(_path_abspath)
    36/12    0.000    0.000    0.000    0.000 _parser.py:178(getwidth)
        3    0.000    0.000    0.000    0.000 <frozen zipimport>:64(__init__)
        6    0.000    0.000    0.000    0.000 argparse.py:1883(_add_action)
       38    0.000    0.000    0.000    0.000 {method 'match' of 're.Pattern' objects}
       18    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:232(__init__)
      239    0.000    0.000    0.000    0.000 {built-in method builtins.getattr}
       17    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:172(_path_isabs)
       18    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:372(release)
        2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:989(create_module)
       33    0.000    0.000    0.000    0.000 typing.py:1215(__setattr__)
        2    0.000    0.000    0.000    0.000 typing.py:1476(__getitem__)
        6    0.000    0.000    0.000    0.000 argparse.py:1704(_add_action)
        2    0.000    0.000    0.000    0.000 enum.py:513(__prepare__)
        2    0.000    0.000    0.000    0.000 {built-in method _imp.create_builtin}
        2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1299(exec_module)
        1    0.000    0.000    0.000    0.000 _compression.py:1(<module>)
       12    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:670(_classify_pyc)
      185    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}
        6    0.000    0.000    0.000    0.000 argparse.py:1595(_get_optional_kwargs)
       19    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:982(find_spec)
        1    0.000    0.000    0.000    0.000 typing.py:515(__getitem__)
        5    0.000    0.000    0.000    0.000 typing.py:1174(__init__)
        2    0.000    0.000    0.000    0.000 {built-in method _imp.exec_dynamic}
      140    0.000    0.000    0.000    0.000 _parser.py:240(__next)
        6    0.000    0.000    0.000    0.000 argparse.py:1512(_add_action)
        1    0.000    0.000    0.000    0.000 typing.py:694(Union)
      207    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:491(_verbose_message)
        2    0.000    0.000    0.000    0.000 argparse.py:1502(add_argument_group)
        7    0.000    0.000    0.000    0.000 dataclasses.py:437(_tuple_str)
        4    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:164(_path_isdir)
        2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:997(exec_module)
        6    0.000    0.000    0.000    0.000 typing.py:166(_type_convert)
        1    0.000    0.000    0.000    0.000 __init__.py:1587(Board)
        3    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1571(__init__)
        2    0.000    0.000    0.000    0.000 typing.py:1485(copy_with)
        2    0.000    0.000    0.000    0.000 {built-in method _imp.exec_builtin}
        2    0.000    0.000    0.000    0.000 argparse.py:1682(__init__)
      169    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}
       24    0.000    0.000    0.000    0.000 <frozen os>:783(encodekey)
      225    0.000    0.000    0.000    0.000 {method 'get' of 'mappingproxy' objects}
       36    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:84(_unpack_uint32)
        3    0.000    0.000    0.000    0.000 dataclasses.py:250(_recursive_repr)
       17    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1128(find_spec)
       35    0.000    0.000    0.000    0.000 enum.py:79(_is_private)
       33    0.000    0.000    0.000    0.000 {built-in method builtins.delattr}
       72    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:134(<genexpr>)
       12    0.000    0.000    0.000    0.000 dataclasses.py:864(_set_new_attribute)
        6    0.000    0.000    0.000    0.000 argparse.py:602(_format_args)
        2    0.000    0.000    0.000    0.000 typing.py:892(__init__)
       18    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:74(__new__)
       12    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:703(_validate_timestamp_pyc)
      107    0.000    0.000    0.000    0.000 {built-in method _imp.release_lock}
        3    0.000    0.000    0.000    0.000 inspect.py:176(get_annotations)
        3    0.000    0.000    0.000    0.000 gettext.py:224(_expand_lang)
        4    0.000    0.000    0.000    0.000 _compiler.py:391(_mk_bitmap)
      104    0.000    0.000    0.000    0.000 {method 'rpartition' of 'str' objects}
       18    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:445(cb)
        4    0.000    0.000    0.000    0.000 functools.py:35(update_wrapper)
        3    0.000    0.000    0.000    0.000 argparse.py:2001(take_action)
       14    0.000    0.000    0.000    0.000 _compiler.py:216(_compile_charset)
       34    0.000    0.000    0.000    0.000 typing.py:1161(_is_dunder)
        7    0.000    0.000    0.000    0.000 {built-in method _abc._abc_init}
        1    0.000    0.000    0.000    0.000 __future__.py:1(<module>)
       36    0.000    0.000    0.000    0.000 enum.py:1543(_get_value)
       71    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1226(__exit__)
       32    0.000    0.000    0.000    0.000 {built-in method builtins.next}
        2    0.000    0.000    0.000    0.000 {built-in method builtins.compile}
      116    0.000    0.000    0.000    0.000 _parser.py:256(match)
       33    0.000    0.000    0.000    0.000 enum.py:784(__delattr__)
       19    0.000    0.000    0.000    0.000 {built-in method _imp.is_builtin}
       14    0.000    0.000    0.000    0.000 _compiler.py:403(_simple)
       73    0.000    0.000    0.000    0.000 {built-in method builtins.min}
       64    0.000    0.000    0.000    0.000 board.py:239(<genexpr>)
       71    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1222(__enter__)
        1    0.000    0.000    0.000    0.000 board.py:825(load_board_class)
        6    0.000    0.000    0.000    0.000 _parser.py:98(closegroup)
       42    0.000    0.000    0.000    0.000 _parser.py:176(append)
       69    0.000    0.000    0.000    0.000 _parser.py:164(__len__)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        4    0.000    0.000    0.000    0.000 enum.py:966(_get_mixins_)
       12    0.000    0.000    0.000    0.000 enum.py:720(__call__)
       46    0.000    0.000    0.000    0.000 {method 'find' of 'bytearray' objects}
       45    0.000    0.000    0.000    0.000 _parser.py:293(tell)
       11    0.000    0.000    0.000    0.000 _parser.py:449(_uniq)
       40    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:67(_relax_case)
       37    0.000    0.000    0.000    0.000 argparse.py:1422(register)
       80    0.000    0.000    0.000    0.000 {built-in method builtins.issubclass}
       18    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:82(remove)
       28    0.000    0.000    0.000    0.000 enum.py:38(_is_descriptor)
       15    0.000    0.000    0.000    0.000 {method 'format' of 'str' objects}
       18    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:79(__init__)
       18    0.000    0.000    0.000    0.000 {built-in method _thread.allocate_lock}
      107    0.000    0.000    0.000    0.000 {built-in method _imp.acquire_lock}
        1    0.000    0.000    0.000    0.000 __init__.py:733(BaseBoard)
        5    0.000    0.000    0.000    0.000 typing.py:262(_collect_parameters)
       48    0.000    0.000    0.000    0.000 {method 'rfind' of 'str' objects}
       21    0.000    0.000    0.000    0.000 {method 'extend' of 'list' objects}
       15    0.000    0.000    0.000    0.000 {built-in method builtins.locals}
        1    0.000    0.000    0.000    0.000 argparse.py:157(HelpFormatter)
       33    0.000    0.000    0.000    0.000 enum.py:48(_is_dunder)
       16    0.000    0.000    0.000    0.000 argparse.py:1426(_registry_get)
        3    0.000    0.000    0.000    0.000 argparse.py:2487(_get_values)
       12    0.000    0.000    0.000    0.000 {built-in method _imp._fix_co_filename}
       17    0.000    0.000    0.000    0.000 {built-in method nt._path_splitroot}
        3    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:662(spec_from_loader)
       12    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:647(_check_name_wrapper)
        3    0.000    0.000    0.000    0.000 dataclasses.py:428(_fields_in_init_order)
       13    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:48(_new_module)
        4    0.000    0.000    0.000    0.000 enum.py:1007(_find_data_type_)
       35    0.000    0.000    0.000    0.000 enum.py:59(_is_sunder)
       10    0.000    0.000    0.000    0.000 {method 'update' of 'dict' objects}
       39    0.000    0.000    0.000    0.000 {method 'pop' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 __init__.py:3961(SquareSet)
        8    0.000    0.000    0.000    0.000 dataclasses.py:404(field)
       73    0.000    0.000    0.000    0.000 {method 'setdefault' of 'dict' objects}
       11    0.000    0.000    0.000    0.000 dataclasses.py:857(_set_qualname)
       24    0.000    0.000    0.000    0.000 <frozen os>:777(check_str)
       20    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:645(parent)
       18    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:173(__exit__)
        6    0.000    0.000    0.000    0.000 argparse.py:1629(_pop_action_class)
        6    0.000    0.000    0.000    0.000 argparse.py:849(__init__)
       51    0.000    0.000    0.000    0.000 {method 'group' of 're.Match' objects}
        4    0.000    0.000    0.000    0.000 argparse.py:955(__init__)
       35    0.000    0.000    0.000    0.000 enum.py:70(_is_internal_class)
        1    0.000    0.000    0.000    0.000 <frozen ntpath>:269(basename)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1336(__init__)
        6    0.000    0.000    0.000    0.000 _parser.py:86(opengroup)
        8    0.000    0.000    0.000    0.000 dataclasses.py:489(_field_init)
        1    0.000    0.000    0.000    0.000 argparse.py:1180(_SubParsersAction)
       14    0.000    0.000    0.000    0.000 {built-in method fromkeys}
        3    0.000    0.000    0.000    0.000 typing.py:730(<genexpr>)
        2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1353(_get_parent_path)
      6/5    0.000    0.000    0.000    0.000 _compiler.py:441(_get_literal_prefix)
        2    0.000    0.000    0.000    0.000 enum.py:1034(_find_new_)
        6    0.000    0.000    0.000    0.000 _parser.py:231(__init__)
       29    0.000    0.000    0.000    0.000 {method 'replace' of 'str' objects}
        1    0.000    0.000    0.000    0.000 <frozen ntpath>:237(split)
       43    0.000    0.000    0.000    0.000 {method 'items' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 __init__.py:586(Piece)
        1    0.000    0.000    0.000    0.000 argparse.py:1135(__init__)
        6    0.000    0.000    0.000    0.000 argparse.py:587(_metavar_formatter)
       10    0.000    0.000    0.000    0.000 _parser.py:372(_escape)
        1    0.000    0.000    0.000    0.000 functools.py:521(decorating_function)
       17    0.000    0.000    0.000    0.000 {built-in method _imp.find_frozen}
        4    0.000    0.000    0.000    0.000 typing.py:1481(<genexpr>)
        4    0.000    0.000    0.000    0.000 argparse.py:2538(_get_value)
       36    0.000    0.000    0.000    0.000 {built-in method from_bytes}
       36    0.000    0.000    0.000    0.000 {method '__exit__' of '_thread.RLock' objects}
       24    0.000    0.000    0.000    0.000 _parser.py:83(groups)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1371(__iter__)
        1    0.000    0.000    0.000    0.000 __init__.py:73(import_module)
        1    0.000    0.000    0.000    0.000 board.py:12(AbstractChessBoard)
        6    0.000    0.000    0.000    0.000 {built-in method time.perf_counter}
       20    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:599(__init__)
        6    0.000    0.000    0.000    0.000 {built-in method _sre.compile}
       10    0.000    0.000    0.000    0.000 enum.py:1187(_generate_next_value_)
       36    0.000    0.000    0.000    0.000 {built-in method _thread.get_ident}
       36    0.000    0.000    0.000    0.000 {method 'isdigit' of 'str' objects}
       16    0.000    0.000    0.000    0.000 typing.py:962(__eq__)
        1    0.000    0.000    0.000    0.000 argparse.py:1013(__init__)
       30    0.000    0.000    0.000    0.000 {method 'add' of 'set' objects}
        6    0.000    0.000    0.000    0.000 enum.py:202(__get__)
       18    0.000    0.000    0.000    0.000 {built-in method _weakref._remove_dead_weakref}
       24    0.000    0.000    0.000    0.000 {method 'upper' of 'str' objects}
        2    0.000    0.000    0.000    0.000 enum.py:956(_check_for_existing_members_)
        2    0.000    0.000    0.000    0.000 _parser.py:312(_class_escape)
       15    0.000    0.000    0.000    0.000 _parser.py:172(__setitem__)
       31    0.000    0.000    0.000    0.000 _parser.py:113(__init__)
       10    0.000    0.000    0.000    0.000 {built-in method builtins.any}
       31    0.000    0.000    0.000    0.000 dataclasses.py:461(<genexpr>)
       40    0.000    0.000    0.000    0.000 {built-in method nt.fspath}
        1    0.000    0.000    0.000    0.000 bz2.py:26(BZ2File)
       36    0.000    0.000    0.000    0.000 enum.py:93(_is_single_bit)
        6    0.000    0.000    0.000    0.000 argparse.py:595(format)
        3    0.000    0.000    0.000    0.000 locale.py:381(normalize)
       20    0.000    0.000    0.000    0.000 enum.py:467(<genexpr>)
        3    0.000    0.000    0.000    0.000 typing.py:317(_deduplicate)
       12    0.000    0.000    0.000    0.000 enum.py:1128(__new__)
       16    0.000    0.000    0.000    0.000 dataclasses.py:683(_is_classvar)
        1    0.000    0.000    0.000    0.000 typing.py:345(_remove_dups_flatten)
        1    0.000    0.000    0.000    0.000 argparse.py:1750(ArgumentParser)
        6    0.000    0.000    0.000    0.000 argparse.py:1642(_check_conflict)
        2    0.000    0.000    0.000    0.000 typing.py:361(_flatten_literal_params)
        2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:501(_requires_builtin_wrapper)
        3    0.000    0.000    0.000    0.000 <frozen abc>:146(update_abstractmethods)
       21    0.000    0.000    0.000    0.000 {method 'lower' of 'str' objects}
        1    0.000    0.000    0.000    0.000 __init__.py:634(Move)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1375(_gcd_import)
        1    0.000    0.000    0.000    0.000 argparse.py:2121(consume_positionals)
        6    0.000    0.000    0.000    0.000 {method 'fileno' of '_io.TextIOWrapper' objects}
       12    0.000    0.000    0.000    0.000 _compiler.py:575(isstring)
        3    0.000    0.000    0.000    0.000 argparse.py:1633(_get_handler)
        1    0.000    0.000    0.000    0.000 argparse.py:1367(_ActionsContainer)
        1    0.000    0.000    0.000    0.000 argparse.py:990(__init__)
        1    0.000    0.000    0.000    0.000 <frozen abc>:121(__subclasscheck__)
       13    0.000    0.000    0.000    0.000 {method 'partition' of 'str' objects}
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1357(_recalculate)
        6    0.000    0.000    0.000    0.000 _parser.py:953(fix_flags)
       64    0.000    0.000    0.000    0.000 __init__.py:296(square_mirror)
        1    0.000    0.000    0.000    0.000 board.py:133(MyBoard)
        9    0.000    0.000    0.000    0.000 {method 'find' of 'str' objects}
        3    0.000    0.000    0.000    0.000 functools.py:65(wraps)
        1    0.000    0.000    0.000    0.000 lzma.py:38(LZMAFile)
        2    0.000    0.000    0.000    0.000 enum.py:383(__init__)
        8    0.000    0.000    0.000    0.000 dataclasses.py:549(_init_param)
        2    0.000    0.000    0.000    0.000 _compiler.py:412(_generate_overlap_table)
       16    0.000    0.000    0.000    0.000 dataclasses.py:691(_is_initvar)
       24    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1577(<genexpr>)
        2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1390(_handle_fromlist)
       18    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:412(__init__)
        1    0.000    0.000    0.000    0.000 typing.py:1205(__getattr__)
        1    0.000    0.000    0.000    0.000 board.py:57(ChessBoard)
       16    0.000    0.000    0.000    0.000 {built-in method builtins.callable}
        9    0.000    0.000    0.000    0.000 typing.py:1279(__eq__)
       18    0.000    0.000    0.000    0.000 {method 'bit_length' of 'int' objects}
        3    0.000    0.000    0.000    0.000 {method 'split' of 'str' objects}
        8    0.000    0.000    0.000    0.000 dataclasses.py:309(__init__)
        2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1343(_find_parent_path_names)
        6    0.000    0.000    0.000    0.000 argparse.py:2320(_parse_optional)
        2    0.000    0.000    0.000    0.000 typing.py:1285(__hash__)
       18    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:158(__init__)
        6    0.000    0.000    0.000    0.000 {method 'lstrip' of 'str' objects}
        6    0.000    0.000    0.000    0.000 argparse.py:206(__init__)
        6    0.000    0.000    0.000    0.000 {method 'values' of 'dict' objects}
        4    0.000    0.000    0.000    0.000 {method 'translate' of 'bytearray' objects}
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1103(_resolve_filename)
       18    0.000    0.000    0.000    0.000 enum.py:819(<genexpr>)
        3    0.000    0.000    0.000    0.000 _compiler.py:472(_get_charset_prefix)
        8    0.000    0.000    0.000    0.000 dataclasses.py:477(_field_assign)
       14    0.000    0.000    0.000    0.000 typing.py:1273(<genexpr>)
        1    0.000    0.000    0.000    0.000 argparse.py:896(BooleanOptionalAction)
       10    0.000    0.000    0.000    0.000 __future__.py:83(__init__)
       10    0.000    0.000    0.000    0.000 {method 'keys' of 'dict' objects}
        3    0.000    0.000    0.000    0.000 argparse.py:984(__call__)
        9    0.000    0.000    0.000    0.000 {method 'sort' of 'list' objects}
        1    0.000    0.000    0.000    0.000 <frozen ntpath>:180(splitroot)
       28    0.000    0.000    0.000    0.000 enum.py:251(__init__)
        6    0.000    0.000    0.000    0.000 enum.py:1291(value)
       16    0.000    0.000    0.000    0.000 dataclasses.py:697(_is_kw_only)
        6    0.000    0.000    0.000    0.000 _parser.py:77(__init__)
       12    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1157(__init__)
        7    0.000    0.000    0.000    0.000 _compiler.py:31(_combine_flags)
        1    0.000    0.000    0.000    0.000 _compression.py:9(BaseStream)
       28    0.000    0.000    0.000    0.000 enum.py:1184(__init__)
        1    0.000    0.000    0.000    0.000 _compression.py:33(DecompressReader)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1158(create_module)
        2    0.000    0.000    0.000    0.000 enum.py:985(_find_data_repr_)
       11    0.000    0.000    0.000    0.000 dataclasses.py:432(<genexpr>)
        1    0.000    0.000    0.000    0.000 {built-in method _abc._abc_subclasscheck}
        7    0.000    0.000    0.000    0.000 typing.py:1630(<genexpr>)
        4    0.000    0.000    0.000    0.000 {built-in method sys.intern}
        2    0.000    0.000    0.000    0.000 typing.py:295(_check_generic)
       17    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:653(has_location)
        7    0.000    0.000    0.000    0.000 typing.py:781(<genexpr>)
        1    0.000    0.000    0.000    0.000 argparse.py:1680(_ArgumentGroup)
       15    0.000    0.000    0.000    0.000 __init__.py:108(<lambda>)
        2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1280(__init__)
       11    0.000    0.000    0.000    0.000 dataclasses.py:1142(<genexpr>)
        3    0.000    0.000    0.000    0.000 argparse.py:2563(_check_value)
        1    0.000    0.000    0.000    0.000 __init__.py:3905(PseudoLegalMoveGenerator)
        4    0.000    0.000    0.000    0.000 _parser.py:166(__delitem__)
        1    0.000    0.000    0.000    0.000 argparse.py:1281(_ExtendAction)
        1    0.000    0.000    0.000    0.000 {built-in method builtins.sorted}
        3    0.000    0.000    0.000    0.000 {built-in method builtins.vars}
        9    0.000    0.000    0.000    0.000 _compiler.py:433(_get_iscased)
       12    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1182(get_filename)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1285(_sanity_check)
        1    0.000    0.000    0.000    0.000 argparse.py:1895(_get_positional_actions)
        1    0.000    0.000    0.000    0.000 argparse.py:1722(_MutuallyExclusiveGroup)
        3    0.000    0.000    0.000    0.000 {method 'items' of 'mappingproxy' objects}
        2    0.000    0.000    0.000    0.000 typing.py:1629(_value_and_type_iter)
        1    0.000    0.000    0.000    0.000 __init__.py:3936(LegalMoveGenerator)
        3    0.000    0.000    0.000    0.000 <frozen abc>:7(abstractmethod)
        1    0.000    0.000    0.000    0.000 enum.py:815(__iter__)
        3    0.000    0.000    0.000    0.000 argparse.py:2410(_get_nargs_pattern)
        1    0.000    0.000    0.000    0.000 __init__.py:142(Outcome)
       11    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:990(create_module)
       10    0.000    0.000    0.000    0.000 enum.py:183(__init__)
        1    0.000    0.000    0.000    0.000 argparse.py:2303(_match_arguments_partial)
        4    0.000    0.000    0.000    0.000 {method '__contains__' of 'frozenset' objects}
        4    0.000    0.000    0.000    0.000 {method 'isidentifier' of 'str' objects}
        1    0.000    0.000    0.000    0.000 functools.py:482(lru_cache)
        4    0.000    0.000    0.000    0.000 __init__.py:429(<genexpr>)
        1    0.000    0.000    0.000    0.000 argparse.py:1152(_VersionAction)
        1    0.000    0.000    0.000    0.000 argparse.py:1292(FileType)
        1    0.000    0.000    0.000    0.000 __future__.py:81(_Feature)
        1    0.000    0.000    0.000    0.000 {method 'rsplit' of 'str' objects}
        1    0.000    0.000    0.000    0.000 argparse.py:109(_AttributeHolder)
        1    0.000    0.000    0.000    0.000 argparse.py:798(Action)
        3    0.000    0.000    0.000    0.000 dataclasses.py:433(<genexpr>)
        1    0.000    0.000    0.000    0.000 argparse.py:953(_StoreAction)
        1    0.000    0.000    0.000    0.000 <frozen ntpath>:36(_get_bothseps)
        1    0.000    0.000    0.000    0.000 argparse.py:1347(Namespace)
        3    0.000    0.000    0.000    0.000 {method 'reverse' of 'list' objects}
        1    0.000    0.000    0.000    0.000 argparse.py:1045(_AppendAction)
        1    0.000    0.000    0.000    0.000 argparse.py:204(_Section)
        1    0.000    0.000    0.000    0.000 argparse.py:727(MetavarTypeHelpFormatter)
        1    0.000    0.000    0.000    0.000 argparse.py:988(_StoreConstAction)
        1    0.000    0.000    0.000    0.000 argparse.py:1083(_AppendConstAction)
        1    0.000    0.000    0.000    0.000 argparse.py:1354(__init__)
        1    0.000    0.000    0.000    0.000 __init__.py:1545(_BoardState)
        1    0.000    0.000    0.000    0.000 argparse.py:1182(_ChoicesPseudoAction)
        1    0.000    0.000    0.000    0.000 argparse.py:1011(_StoreTrueAction)
        1    0.000    0.000    0.000    0.000 argparse.py:1133(_HelpAction)
        1    0.000    0.000    0.000    0.000 {built-in method _imp.get_frozen_object}
        1    0.000    0.000    0.000    0.000 argparse.py:1110(_CountAction)
        2    0.000    0.000    0.000    0.000 {method 'pop' of 'set' objects}
        1    0.000    0.000    0.000    0.000 argparse.py:698(ArgumentDefaultsHelpFormatter)
        1    0.000    0.000    0.000    0.000 argparse.py:769(ArgumentError)
        1    0.000    0.000    0.000    0.000 <string>:1(__create_fn__)
        2    0.000    0.000    0.000    0.000 {built-in method builtins.hash}
        1    0.000    0.000    0.000    0.000 <string>:1(<module>)
        1    0.000    0.000    0.000    0.000 shutil.py:70(SameFileError)
        1    0.000    0.000    0.000    0.000 {built-in method sys._getframemodulename}
        1    0.000    0.000    0.000    0.000 __init__.py:160(InvalidMoveError)
        1    0.000    0.000    0.000    0.000 argparse.py:676(RawDescriptionHelpFormatter)
        1    0.000    0.000    0.000    0.000 argparse.py:687(RawTextHelpFormatter)
        1    0.000    0.000    0.000    0.000 shutil.py:67(Error)
        2    0.000    0.000    0.000    0.000 {built-in method builtins.iter}
        1    0.000    0.000    0.000    0.000 __init__.py:164(IllegalMoveError)
        1    0.000    0.000    0.000    0.000 argparse.py:1028(_StoreFalseAction)
        1    0.000    0.000    0.000    0.000 shutil.py:73(SpecialFileError)
        1    0.000    0.000    0.000    0.000 argparse.py:789(ArgumentTypeError)
        1    0.000    0.000    0.000    0.000 __init__.py:168(AmbiguousMoveError)
        1    0.000    0.000    0.000    0.000 shutil.py:77(ExecError)
        1    0.000    0.000    0.000    0.000 shutil.py:83(RegistryError)
        1    0.000    0.000    0.000    0.000 shutil.py:87(_GiveupOnFastCopy)
        2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1014(is_package)
        1    0.000    0.000    0.000    0.000 shutil.py:80(ReadError)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1412(exec_module)
        1    0.000    0.000    0.000    0.000 dataclasses.py:879(_hash_set_none)


```