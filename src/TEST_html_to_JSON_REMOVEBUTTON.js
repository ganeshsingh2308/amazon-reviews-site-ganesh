const formE20 = document.querySelector('.form1');
const button = document.getElementById('#removeproduct')

formE20.addEventListener('reset',event => {
  event.preventDefault();
  
  const data = new FormData(event.target);

  const value = Object.fromEntries(data.entries());

  value.topics = data.getAll("productdata");

  fetch('http://127.0.0.1:5000/test9',{
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'Access-Control-Allow-Origin': '*'
    },
     body: JSON.stringify(value.topics)
  }).then(res => res.json())
    .then(data => console.log(data))
    .then(window.location.reload())
    .catch(error => console.log(error));
});