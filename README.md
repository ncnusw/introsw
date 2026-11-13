# Introduction to Social Work (社會工作概論)

Classroom games and activities for the course *Introduction to Social Work*, Department of Social Policy and Social Work, National Chi Nan University.

Play them at **https://ncnusw.github.io/introsw/**

## Games

| Game | Folder | Notes |
|---|---|---|
| The Tuesday Club 星期二俱樂部 | `games/tuesday-club/` | Story game, social group work, three classroom pauses |
| Term Duel 名詞對決 | `games/term-duel/` | Whole-class vocabulary duel |
| Storm Over Clear Creek 青溪颱風夜 | `games/storm-creek/` | Story adventure, community work, password-protected. Story, passwords and discussion questions in `tools/story.py`; rebuild `data.js` with `tools/build_data.py`. Opening password: `GATE_PASSWORD` in `index.html` |
| Key Term Tycoon 關鍵詞大亨 | `games/term-tycoon/` | Projector board game for midterm review, **encrypted**: `index.html` is built by `build.py` in the teacher folder (`IntroSW-teacher/term-tycoon/`), which also holds the readable `game.html` and the password. Edit there, rebuild, then push |
| Which Hat? 哪一頂帽子？ | `games/which-hat/` | Supervision role-play for groups of 4 on one phone or tablet: four hats intro, opener, worker scenario, 3-minute timer, observers' check, role switch. 24 scenarios in `SCENARIOS` near the top of `index.html` |
| The Family Next Door 隔壁那一家 | `games/family-next-door/` | Story adventure, social work research. 30-day deadline, two twists, mini-games in `minigames.js` (trash sort, night watch, source detective, interviews, card-sort BSW/MSW exams, town hall); three endings. Opening password `RCT` (`GATE_PASSWORD` in `index.html`). Story, discussion questions and jump codes (`LIBRARY`, `MASTER`, `HOMECOMING`) in `tools/story.py`; maps, terms and exam questions in `tools/build_data.py`, which rebuilds `data.js` |

Story games share `games/engine/` (touch, keyboard and 8BitDo). See the comment at the top of `engine.js` for the script format.
