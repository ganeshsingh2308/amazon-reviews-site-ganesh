const firebaseConfig =
{
  apiKey: "AIzaSyBgBYcGBgX4LRH23dP3hTg7Qv9xoSl938M",
  authDomain: "reviews-dd628.firebaseapp.com",
  databaseURL: "https://reviews-dd628-default-rtdb.europe-west1.firebasedatabase.app/",
  projectId: "reviews-dd628",
  storageBucket: "reviews-dd628.appspot.com",
  messagingSenderId: "1076523572946",
  appId: "1:1076523572946:web:0fd3b378da56bf2873970b",
  measurementId: "G-TR82RMTEEZ"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig)
// firebase.analytics();
const auth = firebase.auth()

function signOut()
{
  auth.signOut();
  alert("Signed Out");
  return "signed out"; 
}


/** Function to check if the authorisation state has changed - used for checking if the user is signed in or not, and then redirecting the user if not signed in */
firebase.auth().onAuthStateChanged(function (user) {
    if (user) {
    // uid = user.uid
    // var user = firebase.auth().currentUser
  
      // firebaseRef.child(uid).set(userData).then((value) =>
      // {
      setTimeout(function () {
      }, 1000)
    } else {
      window.alert('An account has not been detected. Please log in from the homepage, by clicking the login button in the top right.')
      window.location = 'index4.html'
    }
  })
  
  /** DATABASE LINKING - the code below establishes links to different sections of the database */
  database = firebase.database() /** Establish the term 'database' which stores the command to call upon the database */

  const userModuleDataRef = database.ref('/userData/') /** The variable userModuleDataRef stores the command to reference the 'userData' category in the database */
  userModuleDataRef.on('value', gotUserData, errData) /** Reads through the userData category of the database and runs the 'gotUserData' function */

  function gotUserData (data) {
    console.log(data)
    /** grabs current user */
    const user = firebase.auth().currentUser.uid
    console.log(user)
    /** gets the module data values */
    database = firebase.database()
    const userModuleDataRef = database.ref('/userData/').child(user)
    userModuleDataRef.on('value', function (snapshot) {
      document.getElementById('heading1').innerText = ('Hello ' + snapshot.val().userFirstName + ', from business ' + snapshot.val().userBusiness)
    })
    userModuleDataRef.on('value', function (snapshot) {
      document.getElementById('profile_name').innerText = (snapshot.val().userFirstName + ' ' + snapshot.val().userSurname)
    })
    userModuleDataRef.on('value', function (snapshot) {
      document.getElementById('profile_business').innerText = (snapshot.val().userBusiness)
    })}

    let btn = document.querySelector("#sidenav_btn");
    let sidebar = document.querySelector(".sidebar");
    let searchBtn = document.querySelector(".bx-search-alt");
    let logoutBtn = document.querySelector("#logout_btn");

    btn.onclick = function() {
      sidebar.classList.toggle("active");
    }

    searchBtn.onclick = function() {
      sidebar.classList.toggle("active");
    }

    logoutBtn.onclick = function() {
      signOut();
    }



    function errData (err) {
        console.log('Error!')
        console.log(err)
      }
    
