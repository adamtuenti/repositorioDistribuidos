import { Component, OnInit } from '@angular/core';
import * as $ from "jquery";
import { AlertController } from '@ionic/angular';
import { ActivatedRoute, Router } from '@angular/router';
import { environment } from '../../../environments/environment';
@Component({
  selector: 'app-signup',
  templateUrl: './signup.page.html',
  styleUrls: ['./signup.page.scss'],
})
export class SignupPage implements OnInit {
  name: string = "";
  pass1: string = "";
  pass2: string = "";
  apellidos: string = "";
  email: string = "";
  celular: string = "";
  email2: string = "";
  direccion: string = "";
  id: string = "";
  genero: string = "";
  data: any;
  data_aux: any;
  verificado: boolean;
  showpassword: boolean;
  showpassword2: boolean;
  constructor(private alertController: AlertController, private router: ActivatedRoute, private route: Router) {
    this.router.queryParams.subscribe(params => {
      this.data_aux = JSON.parse(params.user);
      this.name = this.data_aux.nombres;
      this.email = this.data_aux.correo;
      this.apellidos = this.data_aux.apellidos;
    })
  }

  ngOnInit() {

  }



  registrar() {
    this.data = {
      nombres: this.name,
      apellidos: this.apellidos,
      identificacion: this.id,
      password: this.pass1,
      correo: this.email,
      correo_alternativo: this.email2,
      telefono: this.celular,
      direccion: this.direccion,
      genero: this.genero
    }
    var self = this;
    var validado = this.validarCampos();
    if (validado && this.verificado) {
      $.post(environment.url + "/api/participante/", this.data)
        .done(function (data) {
          self.alertError("Registro exitoso", "Su cuenta se ha creado exitosamente");
          self.route.navigate(["/educ/home/"]);

        }).fail(function (error) {
          let x = error.responseJSON;
          let isError = false;
          try {
            x["password"][0] != null ? self.alertError("Error al registrarse", x["password"][0]) : isError = true;
            x["correo"][0] != null ? self.alertError("Error al registrarse", x["correo"][0]) : isError = true;
            x["identificacion"][0] != null ? self.alertError("Error al registrarse", x["identificacion"][0]) : isError = true;
          } catch (ex) {
            if (!isError) {
              self.alertError("Error al registrarse", "El registro no fue exitoso");
            }
          }
        });
    }
    if (!validado)
      self.alertError("Campos vacíos", "Debe llenar todos los campos para poder registrarse")

  }

  togglePasswordText() {
    this.showpassword = !this.showpassword;
  }

  togglePasswordText2() {
    this.showpassword2 = !this.showpassword2;
  }

  validarCampos() {
    if (this.name != "" && this.apellidos != "" && this.id != ""
      && this.email != "" && this.genero != "" && this.pass1 != "" && this.pass2 != ""
      && this.celular != "" && this.direccion != "") {
      if (this.pass1 != this.pass2) {
        this.alertError("Verifique su clave", "Las contraseñas no coinciden");
        this.verificado = false;
      }
      else {
        this.verificado = true;
      }


      if (!this.validarCedula(this.id)) {
        this.alertError("Verifique su cédula", "La cédula no es válida");
        this.verificado = false;
      }
      else {
        this.verificado = true;
      }

      return true;
    }
    return false;
  }


  validarCedula(cedula: string) {
    if (cedula.length === 10) {

      // Obtenemos el digito de la region que sonlos dos primeros digitos
      const digitoRegion = cedula.substring(0, 2);
  
      // Pregunto si la region existe ecuador se divide en 24 regiones
      if (digitoRegion >= String(0) && digitoRegion <= String(24)) {
  
        // Extraigo el ultimo digito
        const ultimoDigito = Number(cedula.substring(9, 10));
  
        // Agrupo todos los pares y los sumo
        const pares = Number(cedula.substring(1, 2)) + Number(cedula.substring(3, 4)) + Number(cedula.substring(5, 6)) + Number(cedula.substring(7, 8));
  
        // Agrupo los impares, los multiplico por un factor de 2, si la resultante es > que 9 le restamos el 9 a la resultante
        let numeroUno: any = cedula.substring(0, 1);
        numeroUno = (numeroUno * 2);
        if (numeroUno > 9) {
          numeroUno = (numeroUno - 9);
        }
  
        let numeroTres: any = cedula.substring(2, 3);
        numeroTres = (numeroTres * 2);
        if (numeroTres > 9) {
          numeroTres = (numeroTres - 9);
        }
  
        let numeroCinco: any = cedula.substring(4, 5);
        numeroCinco = (numeroCinco * 2);
        if (numeroCinco > 9) {
          numeroCinco = (numeroCinco - 9);
        }
  
        let numeroSiete: any = cedula.substring(6, 7);
        numeroSiete = (numeroSiete * 2);
        if (numeroSiete > 9) {
          numeroSiete = (numeroSiete - 9);
        }
  
        let numeroNueve: any = cedula.substring(8, 9);
        numeroNueve = (numeroNueve * 2);
        if (numeroNueve > 9) {
          numeroNueve = (numeroNueve - 9);
        }
  
        const impares = numeroUno + numeroTres + numeroCinco + numeroSiete + numeroNueve;
  
        // Suma total
        const sumaTotal = (pares + impares);
  
        // extraemos el primero digito
        const primerDigitoSuma = String(sumaTotal).substring(0, 1);
  
        // Obtenemos la decena inmediata
        const decena = (Number(primerDigitoSuma) + 1) * 10;
  
        // Obtenemos la resta de la decena inmediata - la suma_total esto nos da el digito validador
        let digitoValidador = decena - sumaTotal;
  
        // Si el digito validador es = a 10 toma el valor de 0
        if (digitoValidador === 10) {
          digitoValidador = 0;
        }
  
        // Validamos que el digito validador sea igual al de la cedula
        if (digitoValidador === ultimoDigito) {
          return true;
        } else {
          return false;
        }
  
      } else {
        // imprimimos en consola si la region no pertenece
        return false;
      }
    } else {
      // Imprimimos en consola si la cedula tiene mas o menos de 10 digitos
      return false;
    }
   
  }

  async alertError(msg: string, detalle: any) {
    const alert = await this.alertController.create({
      header: 'Mensaje',
      subHeader: detalle,
      message: msg,
      buttons: ['OK']
    });

    await alert.present();
  }
}
