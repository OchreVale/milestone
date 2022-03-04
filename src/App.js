
import './App.css';
import {useEffect, useState} from 'react'
function App() {
  let [fact, setFact] = useState("")
  function handleClick(){
    fetch("/home",
    {method:"POST",
    headers:{
      "content-type":"application/json",
    }})
    .then(response =>response.json())
    .then(data =>{setFact(data)})
  }
  return (
    <div>
      <p>{fact}</p>
      <button onClick={handleClick}>Click</button>
    </div>
  );
}

export default App;
