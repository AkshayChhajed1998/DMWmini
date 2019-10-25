console.log("Linked")

var submit = document.getElementById('fetch')
var select = document.getElementById('select')

submit.addEventListener("click",function(){
  console.log("Clicked")
  var xhttp = new XMLHttpRequest()
  xhttp.onreadystatechange = function(){
    if(this.readyState===4 && this.status===200){
      document.getElementById('display').innerHTML=this.responseText;
    }
  }
  xhttp.open('POST','/fiapriori/perform/',true)
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("sport="+select.options[select.selectedIndex].value)
})