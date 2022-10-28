$(".burger-menu").click(function(){
	$(".burger-menu__block").toggle(500);
  });
  
const searchBtn = document.querySelector('.nav-right__search img')
let searchInput = document.querySelector('.nav-right__search input')

function clickSearchBtn(){
  let word = searchInput.value
  searchInput.value = ''
  let h1Word = document.querySelector('.analysis-conclusion')
  h1Word.innerText = 'Разбор слова "' + word + '"'
  if (word != '') {
    fetch(
      "https://https://sinonim-antonim.herokuapp.com/api/v1/get_data/" + word
      // "http://localhost:8000/api/v1/get_data/" + word
      , {
        method: "get",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      })
      .then(res => res.json())
      .then(function(json) {
        let slovar = json.slovar
        console.log(slovar)
        synUl = document.querySelector('.analysis-conclusion__block-synonyms__example')
        antUl = document.querySelector('.analysis-conclusion__block-antonyms__example')
        morfUl = document.querySelector('.analysis-conclusion__block-morphemicanalysis__example')
        synUl.innerHTML = ''
        antUl.innerHTML = ''
        morfUl.innerHTML = ''
        for (var i = 0; i < slovar.syn.length; i++) {
          synUl.innerHTML += '<li>' + slovar.syn[i] + '</li>'
        };
        for (var i = 0; i < slovar.antonims.length; i++) {
          antUl.innerHTML += '<li>' + slovar.antonims[i] + '</li>'
        };
        for (var i = 0; i < slovar.morfems.wordComposition.length; i++) {
          morfUl.innerHTML += '<li>' + slovar.morfems.wordComposition[i] + '</li>'
        };
      });
  }


}

searchBtn.addEventListener('click', clickSearchBtn)