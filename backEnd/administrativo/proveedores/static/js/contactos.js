var count = 0;
function contactos() {
  switch(count) {
    case 0:
      a();
      break;
    case 1:
      b();
      break;
    case 2:
      c();
      break;
  }
  count++;
}

function a(){
    document.getElementById("form_contacto_uno").style.display= 'inline';
    // document.getElementById("form_contacto_uno1").style.visibility= 'visible';
    // document.getElementById("form_contacto_uno2").style.visibility= 'visible';
    // document.getElementById("form_contacto_uno3").style.visibility= 'visible';
    // document.getElementById("form_contacto_uno4").style.visibility= 'visible';
    // document.getElementById("form_contacto_uno5").style.visibility= 'visible';
    // document.getElementById("form_contacto_uno6").style.visibility= 'visible';
    // document.getElementById("form_contacto_uno7").style.visibility= 'visible';
}

function b(){
    document.getElementById("form_contacto_dos").style.display= 'inline';
}

function c(){
    document.getElementById("form_contacto_tres").style.display= 'inline';
    document.getElementById("agregar_contacto").style.backgroundColor='white';
}