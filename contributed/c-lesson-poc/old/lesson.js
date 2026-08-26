(() => {
  'use strict';

  const source = `/*
 * Program to calculate the number of cards in the shoe.
 * This code is released under the Vegas Public License.
 * (c)2014, The College Blackjack Team.
 */
#include <stdio.h>

int main()
{
    int decks;
    puts("Enter a number of decks");
    scanf("%i", &decks);
    if (decks < 1) {
        puts("That is not a valid number of decks");
        return 1;
    }
    printf("There are %i cards\\n", (decks * 52));
    return 0;
}
`;

  const prefixThrough = marker => source.slice(0, source.indexOf(marker) + marker.length);

  const lesson = [
    {
      until: prefixThrough('*/\n'),
      lines: [1, 5],
      number: 1,
      title: 'C programs normally begin with a comment.',
      body: 'The comment describes the purpose of the code in the file, and might include some license or copyright information. There’s no absolute need to include a comment here—or anywhere else in the file—but it’s good practice and what most C programmers will expect to find.',
      details: [
        'The comment starts with /*',
        'These *s are optional. They’re only there to make it look pretty.',
        'The comment ends with */.'
      ]
    },
    {
      until: prefixThrough('#include <stdio.h>\n'),
      lines: [6, 6],
      number: 2,
      title: 'Next comes the include section.',
      body: 'C is a very, very small language and it can do almost nothing without the use of external libraries. You will need to tell the compiler what external code to use by including header files for the relevant libraries. The header you will see more than any other is stdio.h. The stdio library contains code that allows you to read and write data from and to the terminal.',
      details: []
    },
    {
      until: source,
      lines: [8, 19],
      number: 3,
      title: 'The last thing you find in a source file are the functions.',
      body: 'All C code runs inside functions. The most important function you will find in any C program is called the main() function. The main() function is the starting point for all of the code in your program.',
      details: []
    }
  ];

  const editor = document.getElementById('editor');
  const playButton = document.getElementById('play');
  const nextButton = document.getElementById('next');
  const resetButton = document.getElementById('reset');
  const speed = document.getElementById('speed');
  const status = document.getElementById('status');
  const noteCard = document.getElementById('noteCard');
  const noteBadge = document.getElementById('noteBadge');
  const noteTitle = document.getElementById('noteTitle');
  const noteBody = document.getElementById('noteBody');
  const detailNotes = document.getElementById('detailNotes');
  const stepLabel = document.getElementById('stepLabel');
  const stepCount = document.getElementById('stepCount');
  const lessonElement = document.getElementById('lesson');
  const connectorPath = document.getElementById('connectorPath');
  const connectorDot = document.getElementById('connectorDot');

  let visible = '';
  let phase = 0;
  let typing = false;
  let pausedAtNote = false;
  let timer = 0;
  let activeRange = null;

  function escapeHtml(value) {
    return value.replace(/[&<>]/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' })[ch]);
  }

  function highlightLine(line, inBlockComment) {
    let result = '';
    let i = 0;
    let block = inBlockComment;

    if (block) {
      const end = line.indexOf('*/');
      if (end === -1) return { html: `<span class="t-comment">${escapeHtml(line)}</span>`, block: true };
      result += `<span class="t-comment">${escapeHtml(line.slice(0, end + 2))}</span>`;
      i = end + 2;
      block = false;
    }

    if (!block && line.slice(i).trimStart().startsWith('#')) {
      return { html: result + `<span class="t-preproc">${escapeHtml(line.slice(i))}</span>`, block: false };
    }

    while (i < line.length) {
      if (line.startsWith('/*', i)) {
        const end = line.indexOf('*/', i + 2);
        if (end === -1) {
          result += `<span class="t-comment">${escapeHtml(line.slice(i))}</span>`;
          block = true;
          break;
        }
        result += `<span class="t-comment">${escapeHtml(line.slice(i, end + 2))}</span>`;
        i = end + 2;
        continue;
      }

      if (line[i] === '"') {
        let j = i + 1;
        while (j < line.length) {
          if (line[j] === '\\') { j += 2; continue; }
          if (line[j] === '"') { j += 1; break; }
          j += 1;
        }
        result += `<span class="t-string">${escapeHtml(line.slice(i, j))}</span>`;
        i = j;
        continue;
      }

      const keyword = line.slice(i).match(/^(int|return|if|void)\b/);
      if (keyword) {
        result += `<span class="t-keyword">${keyword[0]}</span>`;
        i += keyword[0].length;
        continue;
      }

      const number = line.slice(i).match(/^\d+/);
      if (number) {
        result += `<span class="t-number">${number[0]}</span>`;
        i += number[0].length;
        continue;
      }

      result += escapeHtml(line[i]);
      i += 1;
    }

    return { html: result, block };
  }

  function render() {
    const lines = visible.split('\n');
    let blockComment = false;
    const atSourceEnd = visible.length === source.length;
    const html = lines.map((line, index) => {
      const n = index + 1;
      const highlighted = highlightLine(line, blockComment);
      blockComment = highlighted.block;
      const active = activeRange && n >= activeRange[0] && n <= activeRange[1];
      const cursor = typing && !atSourceEnd && index === lines.length - 1 ? '<span class="cursor"></span>' : '';
      return `<div class="code-line${active ? ' active' : ''}" data-line="${n}"><span class="line-no">${n}</span><span class="code-text">${highlighted.html}${cursor}</span></div>`;
    }).join('');

    editor.innerHTML = html;
    editor.scrollTop = editor.scrollHeight;
    requestAnimationFrame(drawConnector);
  }

  function drawConnector() {
    if (!activeRange || window.matchMedia('(max-width: 820px)').matches) {
      connectorPath.setAttribute('d', '');
      connectorDot.setAttribute('cx', '-10');
      connectorDot.setAttribute('cy', '-10');
      return;
    }

    const first = editor.querySelector(`[data-line="${activeRange[0]}"]`);
    const last = editor.querySelector(`[data-line="${activeRange[1]}"]`);
    if (!first || !last) return;

    const stage = lessonElement.getBoundingClientRect();
    const firstBox = first.getBoundingClientRect();
    const lastBox = last.getBoundingClientRect();
    const noteBox = noteCard.getBoundingClientRect();

    const x1 = firstBox.right - stage.left - 14;
    const y1 = ((firstBox.top + lastBox.bottom) / 2) - stage.top;
    const x2 = noteBox.left - stage.left;
    const y2 = noteBox.top - stage.top + 42;
    const spread = Math.max(32, (x2 - x1) * .40);

    connectorPath.setAttribute('d', `M ${x1} ${y1} C ${x1 + spread} ${y1}, ${x2 - spread} ${y2}, ${x2} ${y2}`);
    connectorDot.setAttribute('cx', String(x1));
    connectorDot.setAttribute('cy', String(y1));
  }

  function showNote(item) {
    pausedAtNote = true;
    typing = false;
    activeRange = item.lines;
    noteCard.classList.remove('idle');
    noteCard.classList.add('active');
    noteBadge.textContent = item.number;
    noteTitle.textContent = item.title;
    noteBody.textContent = item.body;
    stepLabel.textContent = `Teaching point ${item.number}`;
    stepCount.textContent = `${item.number} / ${lesson.length}`;
    detailNotes.innerHTML = '';

    if (item.details.length) {
      for (const text of item.details) {
        const div = document.createElement('div');
        div.className = 'detail-note';
        div.textContent = text;
        detailNotes.appendChild(div);
      }
      detailNotes.hidden = false;
    } else {
      detailNotes.hidden = true;
    }

    status.textContent = 'Paused for explanation';
    playButton.textContent = 'Continue';
    render();
  }

  function typeTo(target) {
    if (visible.length >= target.length) {
      showNote(lesson[phase]);
      return;
    }

    typing = true;
    pausedAtNote = false;
    activeRange = null;
    status.textContent = 'Typing prepared source…';
    playButton.textContent = 'Pause';

    const tick = () => {
      if (!typing) return;
      if (visible.length >= target.length) {
        showNote(lesson[phase]);
        return;
      }

      visible += source[visible.length];
      render();

      const typed = visible[visible.length - 1];
      const base = Number(speed.value);
      const delay = typed === '\n' ? base * 3.4 : /[;{}]/.test(typed) ? base * 1.8 : base;
      timer = window.setTimeout(tick, delay);
    };

    tick();
  }

  function continueLesson() {
    if (phase >= lesson.length) return;

    if (pausedAtNote) {
      pausedAtNote = false;
      activeRange = null;
      phase += 1;
      detailNotes.hidden = true;
      noteCard.classList.remove('active');
      if (phase >= lesson.length) {
        status.textContent = 'Lesson complete';
        playButton.textContent = 'Replay';
        stepLabel.textContent = 'Complete';
        render();
        return;
      }
    }

    typeTo(lesson[phase].until);
  }

  function togglePlay() {
    if (phase >= lesson.length) {
      reset();
      continueLesson();
      return;
    }

    if (pausedAtNote) {
      continueLesson();
      return;
    }

    if (typing) {
      typing = false;
      window.clearTimeout(timer);
      status.textContent = 'Paused';
      playButton.textContent = 'Play';
      render();
      return;
    }

    continueLesson();
  }

  function next() {
    if (phase >= lesson.length) return;
    if (typing) {
      typing = false;
      window.clearTimeout(timer);
      visible = lesson[phase].until;
      showNote(lesson[phase]);
      return;
    }
    if (pausedAtNote) continueLesson();
    else continueLesson();
  }

  function reset() {
    typing = false;
    pausedAtNote = false;
    window.clearTimeout(timer);
    visible = '';
    phase = 0;
    activeRange = null;
    status.textContent = 'Ready';
    playButton.textContent = 'Play';
    noteCard.classList.remove('active');
    noteCard.classList.add('idle');
    noteBadge.textContent = '•';
    noteTitle.textContent = 'Prepared code, simulated typing';
    noteBody.textContent = 'Press Play. The source will appear as if typed live. It pauses automatically at each teaching point.';
    detailNotes.hidden = true;
    detailNotes.innerHTML = '';
    stepLabel.textContent = 'Start';
    stepCount.textContent = `0 / ${lesson.length}`;
    render();
  }

  playButton.addEventListener('click', togglePlay);
  nextButton.addEventListener('click', next);
  resetButton.addEventListener('click', reset);
  window.addEventListener('resize', drawConnector);

  document.addEventListener('keydown', event => {
    if (event.target.matches('select, input, textarea, button')) return;
    if (event.code === 'Space') {
      event.preventDefault();
      togglePlay();
    } else if (event.code === 'ArrowRight') {
      event.preventDefault();
      next();
    } else if (event.key.toLowerCase() === 'r') {
      reset();
    }
  });

  reset();
})();
