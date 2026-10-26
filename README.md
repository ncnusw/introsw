# Introduction to Social Work (社會工作概論)

Classroom games and activities for the course *Introduction to Social Work*, Department of Social Policy and Social Work, National Chi Nan University.

Play them at **https://ncnusw.github.io/introsw/**

## Games

| Game | Folder | Notes |
|---|---|---|
| The Tuesday Club 星期二俱樂部 | `games/tuesday-club/` | Story game, social group work (Ch. 5), three classroom pauses |
| Term Duel 名詞對決 | `games/term-duel/` | Whole-class vocabulary duel |
| Storm Over Clear Creek 青溪颱風夜 | `games/storm-creek/` | Story adventure, community work (Ch. 6), password-protected. Story, passwords and discussion questions in `tools/story.py`; rebuild `data.js` with `tools/build_data.py`. Opening password: `GATE_PASSWORD` in `index.html` |
| Key Term Tycoon 關鍵詞大亨 | `games/term-tycoon/` | Projector board game for midterm review, **encrypted**: `index.html` is built by `build.py` in the teacher folder (`IntroSW-teacher/term-tycoon/`), which also holds the readable `game.html` and the password. Edit there, rebuild, then push |

Story games share `games/engine/` (touch, keyboard and 8BitDo). See the comment at the top of `engine.js` for the script format.
