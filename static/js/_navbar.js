function showBalloon(){
  var wObjballoon2	= document.getElementById("balloon2");
  // 吹き出しの表示／非表示制御（クラス変更）
  if (wObjballoon2.className == "sample22"){
  	wObjballoon2.className = "sample21";
  }else{
  	wObjballoon2.className = "sample22";
  }
}