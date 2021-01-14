import { Component, OnInit } from '@angular/core';
import { NavigationExtras, Router } from '@angular/router';
import { GooglePlus } from '@ionic-native/google-plus/ngx';
import { AngularFireAuth } from '@angular/fire/auth';
import * as firebase from 'firebase/app';
import { Platform } from '@ionic/angular';
import { Facebook, FacebookLoginResponse } from '@ionic-native/facebook/ngx';
import { AppComponent } from "../../app.component";
import * as $ from "jquery";
import { AlertController } from '@ionic/angular';
import { environment } from '../../../environments/environment';
import { MessagingService } from '../../services/messaging.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})

export class LoginPage implements OnInit {
  loading: any;
  id_user: string;
  email: string = "";
  pass: string = "";
  showpassword: boolean;
  constructor(
    private router: Router,
    private platform: Platform,
    private google: GooglePlus,
    private fireAuth: AngularFireAuth,
    private fb: Facebook,
    private App: AppComponent,
    private alertController: AlertController,
    private messagingService: MessagingService
  ) {

  }

  ngOnInit() {

  }


  async login() {
    var data = {
      "correo": this.email,
      "clave": this.pass
    }
    var self = this;
    var url = environment.url + "/api/login_participante/"
    await $.post(url, data).done(function (user) {
      if (!user.error) {
        self.App.id_User = user.id;
        self.habilitarOpciones();
        self.App.storage.set("user", data.correo);
        self.App.storage.set("pass", data.clave);
        self.App.storage.set("id", user.id);
        self.requestPermission(user.id);
      }
      else {
        self.alertError(user.mensaje, "Credenciales incorrectas");
      }
    });
  }

  requestPermission(id_User:string) {
    this.messagingService.requestPermission(id_User).subscribe(
      async token => {
          this.listenForMessages();
      },
      async (err) => {
        const alert = await this.alertController.create({
          header: 'Error',
          message: err,
          buttons: ['OK'],
        });
 
        await alert.present();
      }
    );
  }

 listenForMessages() {
    this.messagingService.getMessages().subscribe(async (msg: any) => {
      const alert = await this.alertController.create({
        header: msg.notification.title,
        subHeader: msg.notification.body,
        message: msg.data.info,
        buttons: ['OK'],
      });
 
      await alert.present();
    });
  }

  async verificarCuenta(res: any) {
    var self = this;

    var data = {
      "correo": res['email'],
      "nombres": res['given_name'],
      "apellidos": res['family_name']
    }
    await $.post(environment.url + "/api/existe_participante/", data).done(function (user) {
      if (!user.error) {
        self.App.id_User = user.id;
        self.habilitarOpciones();
      }
      else {
        let navigationExtras: NavigationExtras = {
          queryParams: {
            user: JSON.stringify(data)
          }
        };
        self.alertError("Complete los datos faltantes para completar su registro", "Inicio exitoso");
        self.router.navigate(["/signup/"], navigationExtras);
      }
    })
  }

  async loginGoogle() {
    let params;
    if (this.platform.is('android')) {
      params = {
        'webClientId': '44397923925-udqfaidjvqhp8p7ule0oihpn4i3co6je.apps.googleusercontent.com',
        'offline': true
      }
      this.google.login(params)
        .then((response) => {
          const { idToken, accessToken } = response
          this.onLoginSuccess(idToken, accessToken);
        }).catch((error) => {
          console.log(error)
          alert('error:' + JSON.stringify(error))
        });
    }
    else {
      this.loginGoogleWeb();
    }
  }

  loginFacebook() {
    if (this.platform.is('android')) {
      this.loginFacebookAndroid();
    } else {
      this.loginFacebookWeb();
    }
  }

  togglePasswordText() {
    this.showpassword = !this.showpassword;
}

  async loginGoogleWeb() {
    const res = await this.fireAuth.auth.signInWithPopup(new firebase.auth.GoogleAuthProvider());
    this.verificarCuenta(res.additionalUserInfo.profile);
  }

  async loginFacebookAndroid() {
    const res: FacebookLoginResponse = await this.fb.login(['public_profile', 'email']);
    const facebookCredential = firebase.auth.FacebookAuthProvider.credential(res.authResponse.accessToken);
    const resConfirmed = await this.fireAuth.auth.signInWithCredential(facebookCredential);
    this.verificarCuenta(resConfirmed.additionalUserInfo.profile);
  }

  async loginFacebookWeb() {
    const res = await this.fireAuth.auth.signInWithPopup(new firebase.auth.FacebookAuthProvider());
    this.verificarCuenta(res.additionalUserInfo.profile);
  }

  onLoginSuccess(accessToken, accessSecret) {
    const credential = accessSecret ? firebase.auth.GoogleAuthProvider
      .credential(accessToken, accessSecret) : firebase.auth.GoogleAuthProvider
        .credential(accessToken);
    this.fireAuth.auth.signInWithCredential(credential)
      .then((response) => {
        this.verificarCuenta(response.additionalUserInfo.profile);
      })
  }



  habilitarOpciones() {
    this.App.estadoUser = true;
    for (let i = 0; i < this.App.listMenu.length; i++) {
      this.App.listMenu[i].disable = false;
    }

    for (let i = 0; i < this.App.listTabs.length; i++) {
      this.App.listTabs[i].disable = false;
    }
    this.router.navigate(["/educ/home/"]);
  }

  async alertError(msg: string, msg2: string) {
    const alert = await this.alertController.create({
      header: msg2,
      message: msg,
      buttons: ['OK']
    });

    await alert.present();
  }

}

