const GRAFIK = {
  "понедельник": "Тимур",
  "вторник": "Глеб",
  "среда": "Вера"
};

// дежурный: возвращает имя дежурного в указанный день или пустую строку
function dezhurnyj(den, grafik) {
  if (grafik.hasOwnProperty(den)) {
    return grafik[den];
  }
  return "";
}

if (typeof module !== 'undefined') module.exports = { GRAFIK, dezhurnyj };
