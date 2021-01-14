import { Injectable } from '@angular/core';
import { AngularFireMessaging } from '@angular/fire/messaging';
import { tap } from 'rxjs/operators'
import { environment } from '../../environments/environment';
import * as $ from "jquery";

@Injectable({
  providedIn: 'root'
})
export class MessagingService {

  token = null;

  constructor(private afMessaging: AngularFireMessaging) { }

  requestPermission(idUser:string) {
    return this.afMessaging.requestToken.pipe(
      tap(token => {
        var data = { "token": token,"id_participante":idUser}
        console.log(data)
        $.post(environment.url + "/api/token_notificacion/", data)
          .done(function (res) {
            console.log("OK")
          })
      }));
  }

  getMessages() {
    return this.afMessaging.messages;
  }

  deleteToken() {
    if (this.token) {
      this.afMessaging.deleteToken(this.token);
      this.token = null;
    }
  }
}
