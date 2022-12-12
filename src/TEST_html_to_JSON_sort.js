const formE14 = document.querySelector('.form4');

formE14.addEventListener('submit',event => {
  event.preventDefault();
  
  var value = document.getElementById('keywordid').innerText;

  fetch('http://127.0.0.1:5000/test8',{
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'Access-Control-Allow-Origin': '*'
    },
     body: JSON.stringify(value)
  }).then(res => res.json())
    .then(data => console.log(data))
    .then(window.location.reload())
    .catch(error => console.log(error));
});

const formE15 = document.querySelector('.form5');

formE15.addEventListener('submit',event => {
  event.preventDefault();
  
  var value = document.getElementById('keywordid1').innerText;

  fetch('http://127.0.0.1:5000/test8',{
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'Access-Control-Allow-Origin': '*'
    },
     body: JSON.stringify(value)
  }).then(res => res.json())
    .then(data => console.log(data))
    .then(window.location.reload())
    .catch(error => console.log(error));
});

const formE16 = document.querySelector('.form6');

formE16.addEventListener('submit',event => {
  event.preventDefault();
  
  var value = document.getElementById('keywordid2').innerText;

  fetch('http://127.0.0.1:5000/test8',{
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'Access-Control-Allow-Origin': '*'
    },
     body: JSON.stringify(value)
  }).then(res => res.json())
    .then(data => console.log(data))
    .then(window.location.reload())
    .catch(error => console.log(error));
});

const formE17 = document.querySelector('.form7');

formE17.addEventListener('submit',event => {
  event.preventDefault();
  
  var value = document.getElementById('keywordid3').innerText;

  fetch('http://127.0.0.1:5000/test8',{
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'Access-Control-Allow-Origin': '*'
    },
     body: JSON.stringify(value)
  }).then(res => res.json())
    .then(data => console.log(data))
    .then(window.location.reload())
    .catch(error => console.log(error));
});

const formE18 = document.querySelector('.form8');

formE18.addEventListener('submit',event => {
  event.preventDefault();
  
  var value = document.getElementById('keywordid4').innerText;

  fetch('http://127.0.0.1:5000/test8',{
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'Access-Control-Allow-Origin': '*'
    },
     body: JSON.stringify(value)
  }).then(res => res.json())
    .then(data => console.log(data))
    .then(window.location.reload())
    .catch(error => console.log(error));
});