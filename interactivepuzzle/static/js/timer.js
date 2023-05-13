function timer() {
  var dateObject = moment(startTime, "MMMM D, YYYY, h:mm a").toDate();
  var currentTime = new Date();
  var minutes = parseInt((currentTime - dateObject) / (1000 * 60));
  document.getElementById(
    "timer"
  ).innerHTML = `<p class = "timer_p" style = "margin:"none";color:green;">Time Taken :${minutes} minutes</p>`;
}
timer();
setInterval(() => {
  timer();
}, 60 * 1000);
