// console.log("Hello")
let characterCount=0;
textarea.addEventListener("keydown",(e)=>{
     text=e.target.value;
     let words=text.trim(" ").split(" ").filter(word => word != ' ')
        if(words[0]===""){
wordCounter=0
        }
        else{
            wordCounter=words.length
        }
   const longestWord= (words)=> {
  return words.reduce((c, v) => c.length > v.length ? c : v);
}
longestWordDisplay.textContent=longestWord(words)
if(text.length!=0){
characterCount=text.length+1}
else{
    characterCount=text.length
}
wordCount.textContent=wordCounter
letterCount.textContent=characterCount
})