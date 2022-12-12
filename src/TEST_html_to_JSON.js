const formE1 = document.querySelector('.form');

formE1.addEventListener('submit',event => {
  event.preventDefault();
  const formData = new FormData(formE1);
  const data = Object.fromEntries(formData);
  document.getElementById("amazonlink").disabled = true;
  document.getElementById('loadingbar').innerText = 'LOADING'
  

  fetch('http://127.0.0.1:5000',{
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'Access-Control-Allow-Origin': '*'
    },
     body: JSON.stringify(data)
  }).then(res => res.json())
    .then(data => document.getElementById('loadingbar').innerText = data)
    .then(data => document.getElementById("amazonlink").disabled = false)
    .then(data => console.log(data))
    .catch(error => console.log(error));
});