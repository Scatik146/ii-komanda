
// график: данные — кто в какой день дежурит

const GRAFIK = \[

&#x20; { den: "понедельник", kto: "Тимур" },

&#x20; { den: "вторник", kto: "Глеб" },

&#x20; { den: "среда", kto: "Вера" }

];



// dezhurnyj: имя дежурного в этот день или пустая строка

function dezhurnyj(den, grafik) {

&#x20; const zapis = najtiZapis(den, grafik);

&#x20; return imjaDezhurnogo(zapis);

}



// najtiZapis: запись графика для этого дня или null

function najtiZapis(den, grafik) {

&#x20; for (let i = 0; i < grafik.length; i++) {

&#x20;   if (grafik\[i].den === den) {

&#x20;     return grafik\[i];

&#x20;   }

&#x20; }

&#x20; return null;

}



// imjaDezhurnogo: имя из записи или пустая строка

function imjaDezhurnogo(zapis) {

&#x20; if (zapis === null) {

&#x20;   return "";

&#x20; }

&#x20; return zapis.kto;

}



if (typeof module !== 'undefined') module.exports = { GRAFIK, dezhurnyj };

