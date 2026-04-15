(function () {
  'use strict';

  var POINTS = 5;
  var N = 20;
  var LS_KEY = 'ilkyardimSinavSonuclari_v1';

  function scoreMapRead() {
    try {
      var s = localStorage.getItem(LS_KEY);
      if (!s) return {};
      var o = JSON.parse(s);
      return typeof o === 'object' && o !== null ? o : {};
    } catch (e) {
      return {};
    }
  }

  function scoreMapWrite(map) {
    try {
      localStorage.setItem(LS_KEY, JSON.stringify(map));
    } catch (e) {}
  }

  function resultKey(bank, exam) {
    return bank + ':' + String(exam.id != null ? exam.id : '');
  }

  function saveQuizResult(bank, exam, score, maxScore) {
    var m = scoreMapRead();
    m[resultKey(bank, exam)] = { score: score, max: maxScore, at: Date.now() };
    scoreMapWrite(m);
  }

  function getQuizResult(bank, exam) {
    return scoreMapRead()[resultKey(bank, exam)] || null;
  }

  function clearQuizResults() {
    try {
      localStorage.removeItem(LS_KEY);
    } catch (e) {}
  }

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

  var currentBank = 'ilkyardim';

  function getExams() {
    var raw =
      currentBank === 'meb' ? window.MEB_EXAMS : window.ILKYARDIM_EXAMS;
    if (!Array.isArray(raw) || raw.length === 0) return null;
    return raw;
  }

  function updateTabActive() {
    document.querySelectorAll('[data-bank-tab]').forEach(function (btn) {
      var on = btn.getAttribute('data-bank-tab') === currentBank;
      btn.classList.toggle('exam-type-tab--active', on);
      btn.setAttribute('aria-selected', on ? 'true' : 'false');
    });
  }

  function renderExamList() {
    var exams = getExams();
    var listEl = byId('exam-list');
    var errHome = byId('home-error');
    show(errHome, false);

    if (!exams) {
      errHome.textContent =
        currentBank === 'meb'
          ? 'MEB soru bankası yüklenemedi (assets/meb-veriler.js eksik).'
          : 'Sınav verisi yok. assets/veriler.js dosyası yüklü mü kontrol et.';
      show(errHome, true);
      listEl.innerHTML = '';
      return;
    }

    for (var i = 0; i < exams.length; i++) {
      var v = validateExam(exams[i]);
      if (v) {
        errHome.textContent = v;
        show(errHome, true);
        listEl.innerHTML = '';
        return;
      }
    }

    listEl.innerHTML = '';
    for (var j = 0; j < exams.length; j++) {
      (function (exam) {
        var li = document.createElement('li');
        li.className = 'exam-card';
        var prev = getQuizResult(currentBank, exam);
        if (prev) li.classList.add('exam-card--completed');

        var head = document.createElement('div');
        head.className = 'exam-card-head';
        var h2 = document.createElement('h2');
        h2.textContent = exam.title;
        head.appendChild(h2);
        var isKarma =
          currentBank === 'ilkyardim' &&
          (String(exam.id) === '6' ||
            (exam.title && String(exam.title).indexOf('Karma') !== -1));
        if (isKarma) {
          var pill = document.createElement('span');
          pill.className = 'pill pill--new';
          pill.textContent = 'Yeni';
          pill.setAttribute('aria-label', 'Yeni set');
          head.appendChild(pill);
        }
        li.appendChild(head);

        if (prev) {
          var scoreP = document.createElement('p');
          scoreP.className = 'exam-card-last-score';
          scoreP.textContent = 'Son not: ' + prev.score + ' / ' + prev.max;
          li.appendChild(scoreP);
        }

        var p = document.createElement('p');
        p.textContent = N + ' soru';
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'btn btn-primary';
        btn.textContent = 'Başla';
        btn.addEventListener('click', function () {
          startQuiz(exam);
        });
        li.appendChild(p);
        li.appendChild(btn);
        listEl.appendChild(li);
      })(exams[j]);
    }
  }

  var bankTabsBound = false;

  function setupBankTabs() {
    if (bankTabsBound) return;
    bankTabsBound = true;
    document.querySelectorAll('[data-bank-tab]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var bank = btn.getAttribute('data-bank-tab');
        if (bank === currentBank) return;
        if (byId('view-quiz') && !byId('view-quiz').classList.contains('hidden')) {
          goHome();
        }
        currentBank = bank;
        updateTabActive();
        renderExamList();
      });
    });
  }

  function goHome() {
    show(byId('view-quiz'), false);
    show(byId('view-home'), true);
    renderExamList();
  }

  var resetBound = false;

  function setupResetScores() {
    if (resetBound) return;
    resetBound = true;
    var b = byId('btn-reset-scores');
    if (!b) return;
    b.addEventListener('click', function () {
      if (
        !confirm(
          'Kayıtlı tüm sınav notlarını silmek istiyor musun? Bu işlem geri alınamaz.'
        )
      ) {
        return;
      }
      clearQuizResults();
      renderExamList();
    });
  }

  function init() {
    setupBankTabs();
    setupResetScores();
    updateTabActive();
    renderExamList();
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
        saveQuizResult(currentBank, exam, score, maxScore);
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
