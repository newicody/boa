/* loader */
/* send pool structure */
/* query auth */

class auth {
  constructor(login,password) {
    this.login = login;
    this.password = password;
    //proxy list
    this.server_list = ["192.168.1.158:8080","192.168.1.158:8080"];
  }
  query_first() {
     // select from the proxy list most reactif server
     let myhead = new Headers();
  //      myhead.append('Content-Type', 'text/html');
 //       myhead.append("Access-Control-Allow-Origin", "*")
 //       myhead.append("Access-Control-Allow-Headers","Content-Type");
 //       myhead.append('Access-Control-Allow-Credentials', true);
//        myhead.append('Access-Control-Allow-Methods', 'GET POST');
       // myhead.append('Origin', '192.168.1.158:8080'),
 //       myhead.append('charset','UTF-8');

     let requestOptions = {
//  host: 'aabc.com',
//  mode: "cors",
//  cache: "default",
  method: 'POST',
  headers: myhead,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
  body: JSON.stringify({login: this.login, password: this.password}),
// credentials: "include",


//  redirect: "manual",
//  referrerPolicy: "no-referrer",
};

//     this.server_list.forEach(ip => fetch("http://" + ip + "/auth.php", requestOptions).then((res) => res.text().then((res) => {document.write(res)})  ));
     this.server_list.forEach(ip => fetch("http://" + ip + "/auth.php",requestOptions).then((res) => res.text().then((res) => {document.write(res)})  ));

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
    this.validate.setAttribute('type','button');
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
myform.validate.onclick = function(){myform.validate_form(myform.login.value,myform.password.value );};
