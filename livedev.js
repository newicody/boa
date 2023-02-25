/* loader */
/* send pool structure */
/* query auth */

class auth {
  constructor(login,password) {
    this.login = login;
    this.password = password;
    this.server_list = ['192.168.1.10','192.168.1.12','192.168.1.12'];
  }
  query_first() {
     this.server_list.forEach(ip => fetch('https://'+ip+'/auth.php?login='+this.login+'&password='+this.password).then((res) => { alert(res); return res; }));
  }
}
class form {
  constructor(target) {
    this.target = target;
    this.login = '';
    this.password = '';
    this.validate = '' ;
  }
  validate_form(login,password) {
    let send_form = new auth(login,password);
    send_form.query_first();
  }
  draw_form() {
    let formulaire = document.createElement('form');

    this.login = document.createElement('input');
    this.password = document.createElement('input');

    this.validate = document.createElement('input');
    this.validate.setAttribute('type','submit');
    this.validate.setAttribute('value','Send');

    formulaire.appendChild(this.login);
    formulaire.appendChild(this.password);
    formulaire.appendChild(this.validate);


    document.getElementById(this.target).appendChild(formulaire);
  }
}

// Formulaire's creation
let myform = new form('form');
// Adding input and button
myform.draw_form();
// event onclick : send auth
myform.validate.onclick = function(){myform.validate_form(myform.login.value,myform.password.value);};
