(function () {
  'use strict';

  var POINTS = 5;
  var N = 20;

  function show(el, on) {
    if (!el) return;
    el.classList.toggle('hidden', !on);
  }

  function byId(id) {
    return document.getElementById(id);
  }

  /** Şık metinlerini karıştırır; doğru cevabın yeni indeksini döner. */
  function shuffleOptions(options, correctOrigIndex) {
    var entries = options.map(function (label, orig) {
      return { label: label, orig: orig };
    });
    for (var k = entries.length - 1; k > 0; k--) {
      var j = Math.floor(Math.random() * (k + 1));
      var t = entries[k];
      entries[k] = entries[j];
      entries[j] = t;
    }
    var displayCorrect = -1;
    for (var i = 0; i < entries.length; i++) {
      if (entries[i].orig === correctOrigIndex) {
        displayCorrect = i;
        break;
      }
    }
    return { entries: entries, displayCorrect: displayCorrect };
  }

  function validateExam(exam) {
    if (!exam || !Array.isArray(exam.questions)) return 'Sınav verisi yok.';
    if (exam.questions.length !== N) return 'Bu sınavda ' + N + ' soru olmalı.';
    for (var i = 0; i < exam.questions.length; i++) {
      var q = exam.questions[i];
      if (!q || typeof q.text !== 'string' || !String(q.text).trim()) return 'Soru ' + (i + 1) + ' metni eksik.';
      if (!Array.isArray(q.options) || q.options.length < 2) return 'Soru ' + (i + 1) + ' şıkları eksik.';
      if (typeof q.correct !== 'number' || q.correct < 0 || q.correct >= q.options.length) {
        return 'Soru ' + (i + 1) + ' doğru indeksi hatalı.';
      }
    }
    return null;
  }

  function getExams() {
    var raw = window.ILKYARDIM_EXAMS;
    if (!Array.isArray(raw) || raw.length === 0) return null;
    return raw;
  }

  function goHome() {
    show(byId('view-quiz'), false);
    show(byId('view-home'), true);
  }

  function init() {
    var exams = getExams();
    var listEl = byId('exam-list');
    var errHome = byId('home-error');

    if (!exams) {
      errHome.textContent = 'Sınav verisi yok. assets/veriler.js dosyası yüklü mü kontrol et.';
      show(errHome, true);
      return;
    }

    for (var i = 0; i < exams.length; i++) {
      var v = validateExam(exams[i]);
      if (v) {
        errHome.textContent = v;
        show(errHome, true);
        return;
      }
    }

    listEl.innerHTML = '';
    for (var j = 0; j < exams.length; j++) {
      (function (exam) {
        var li = document.createElement('li');
        li.className = 'exam-card';
        var h2 = document.createElement('h2');
        h2.textContent = exam.title;
        var p = document.createElement('p');
        p.textContent = N + ' soru · en fazla ' + N * POINTS + ' puan';
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'btn btn-primary';
        btn.textContent = 'Başla';
        btn.addEventListener('click', function () {
          startQuiz(exam);
        });
        li.appendChild(h2);
        li.appendChild(p);
        li.appendChild(btn);
        listEl.appendChild(li);
      })(exams[j]);
    }
  }

  function startQuiz(exam) {
    var err = validateExam(exam);
    if (err) {
      alert(err);
      return;
    }

    show(byId('view-home'), false);
    show(byId('view-quiz'), true);
    byId('quiz-title').textContent = exam.title || 'Sınav';
    show(byId('quiz-error'), false);
    show(byId('quiz-active'), true);
    show(byId('quiz-result'), false);

    var state = {
      questions: exam.questions,
      index: 0,
      correct: 0,
      answered: false,
    };

    var progressLabel = byId('progress-label');
    var progressFill = byId('progress-fill');
    var questionText = byId('question-text');
    var optionsList = byId('options-list');
    var feedbackEl = byId('feedback');
    var btnNext = byId('btn-next');

    function renderQ() {
      state.answered = false;
      var q = state.questions[state.index];
      questionText.textContent = q.text;
      optionsList.innerHTML = '';
      show(feedbackEl, false);
      btnNext.disabled = true;
      btnNext.textContent = state.index === N - 1 ? 'Bitir' : 'Sonraki';

      var prog = state.index + 1;
      progressLabel.textContent = 'Soru ' + prog + ' / ' + N;
      progressFill.style.width = (prog / N) * 100 + '%';

      var shuffled = shuffleOptions(q.options, q.correct);
      state.displayCorrect = shuffled.displayCorrect;

      shuffled.entries.forEach(function (item, idx) {
        var li = document.createElement('li');
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'option-btn';
        b.textContent = item.label;
        b.dataset.index = String(idx);
        b.addEventListener('click', onPick);
        li.appendChild(b);
        optionsList.appendChild(li);
      });
    }

    function onPick(ev) {
      if (state.answered) return;
      var btn = ev.currentTarget;
      var picked = parseInt(btn.dataset.index, 10);
      var ok = state.displayCorrect;
      state.answered = true;
      if (picked === ok) state.correct++;

      optionsList.querySelectorAll('.option-btn').forEach(function (b) {
        b.disabled = true;
        var i = parseInt(b.dataset.index, 10);
        b.classList.add('revealed');
        if (i === ok) b.classList.add('correct-answer');
        if (i === picked && picked !== ok) b.classList.add('wrong-pick');
        if (i === picked && picked === ok) b.classList.add('correct-pick');
      });

      show(feedbackEl, true);
      if (picked === ok) {
        feedbackEl.textContent = 'Doğru';
        feedbackEl.classList.remove('bad');
        feedbackEl.classList.add('ok');
      } else {
        feedbackEl.textContent = 'Yanlış';
        feedbackEl.classList.remove('ok');
        feedbackEl.classList.add('bad');
      }
      btnNext.disabled = false;
    }

    btnNext.onclick = function () {
      if (!state.answered) return;
      if (state.index < N - 1) {
        state.index++;
        renderQ();
      } else {
        show(byId('quiz-active'), false);
        show(byId('quiz-result'), true);
        var score = state.correct * POINTS;
        var maxScore = N * POINTS;
        byId('result-total').textContent = 'Toplam puan: ' + score;
        byId('result-score').textContent = score + ' / ' + maxScore;
        byId('result-detail').textContent = state.correct + ' doğru · ' + (N - state.correct) + ' yanlış';
      }
    };

    byId('btn-retry').onclick = function () {
      startQuiz(exam);
    };

    renderQ();
  }

  byId('btn-ana').addEventListener('click', goHome);
  byId('btn-ana2').addEventListener('click', goHome);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
