const formE13 = document.querySelector('.form3');

formE13.addEventListener('submit',event => {
  event.preventDefault();
  const formData = new FormData(formE13);
  const data = Object.fromEntries(formData);

  fetch('http://127.0.0.1:5000/test7',{
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'Access-Control-Allow-Origin': '*'
    },
     body: JSON.stringify(data)
  }).then(res => res.json())
    .then(window.location.reload())
    .then(data => console.log(data))
    .catch(error => console.log(error));
});