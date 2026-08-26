# Interactive C lesson proof of concept

This is a self-contained browser demonstration based on the supplied textbook image.

## Run

Open `index.html` in a browser. No server, package manager, build step, or Internet connection is required.

On Linux, for example:

```sh
xdg-open index.html
```

## Controls

- **Play**: start/resume simulated typing.
- **Pause**: stop typing at the current character.
- **Continue**: advance after an explanatory pause.
- **Next**: while typing, jump immediately to the next teaching point; while paused, continue to the next section.
- **Reset**: return to the beginning.
- Keyboard: `Space` = play/pause/continue, `Right Arrow` = next, `R` = reset.

## Structure

- `index.html`: page structure.
- `style.css`: responsive editor and annotation layout.
- `lesson.js`: prepared source code, animation state machine, annotations and connector.
- `cards.c`: C source from the example.

The lesson data is near the top of `lesson.js`. To make a new lesson, replace `source` and the entries in `lesson`.
