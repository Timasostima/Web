const photos = document.getElementsByClassName("behind-image")

let clicked = function(){
  const actualPhoto = this.nextElementSibling
  actualPhoto.classList.toggle("clicked")
}
let mouseleave = function(){
  const actualPhoto = this.nextElementSibling
  actualPhoto.classList.remove("clicked")
}
for (let i= 0; i<photos.length;i++){
  photos[i].addEventListener('click', clicked)
  photos[i].addEventListener('mouseleave', mouseleave)
}
