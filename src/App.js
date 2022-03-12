
import './style_review.css';
import {useEffect, useState} from 'react'
function App() {
  const params = window.location.search
  let[youtube_link, setYT] = useState()
  let[title, setTitle] = useState()
  let[comments, getComments] = useState([])
  let [user, setuser] = useState()
  let [score, setScore] = useState()
  const action = `react${params}`;
  useEffect( async() =>{
    const response = await fetch(`/react${params}`);
    const data = await response.json()
    getComments(data["comments"]);
    setTitle(data["title"]);
    setYT(data["youtube"]);
    setuser(data["current_user"]);
    setScore(data["rating"])
  }, [])
  const dlt = `delete${params}&cid=${user}`
  console.log(comments)
  return (
    <div>
      <h2>{title}:{score}/10</h2>
      <div class = "embedding">
      <iframe width="560" height="315" src={youtube_link}
        title="YouTube video player" frameborder="0" allow="accelerometer; 
        autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen></iframe>
      </div>
      <div class ="form">
        <form action= {action} method='POST'>
          <label>Review this movie</label><br></br>
          <textarea name='comments' required class="text"></textarea><br></br>
          <label>Rate this movie</label><br></br>
          <input type={"number"} required name="rating" min={1} max={10} class="rating"></input><br></br>
          <input type={"submit"} value="submit"></input>
        </form>
        </div>
        <div class="message">
          <div class="row">
            <div class ="col">
            {comments.map(element =><div class="comment"><p>{element}</p></div> )}
            </div>
          </div>
          </div>
          <form action={dlt} method='POST'>
        <input type="submit" value="Delete your comment"></input>
      </form>
    </div>
  );
}
export default App;
