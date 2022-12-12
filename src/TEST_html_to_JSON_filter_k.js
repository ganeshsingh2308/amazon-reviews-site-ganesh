const formE2 = document.querySelector('.form2');

formE2.addEventListener('submit',event => {
  event.preventDefault();
  
  const data = new FormData(event.target);

  const value = Object.fromEntries(data.entries());

  value.topics = data.getAll("productdata");

  fetch('http://127.0.0.1:5000/test5',{
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'Access-Control-Allow-Origin': '*'
    },
     body: JSON.stringify(value.topics)
  }).then(res => res.json())
    .then(window.location.reload())
    .then(data => console.log(data))
    .catch(error => console.log(error));
});