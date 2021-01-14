import { Component, OnInit } from '@angular/core';
import { AlertController } from '@ionic/angular';
import { Router } from '@angular/router';
import { AppComponent } from '../app.component';
import * as $ from "jquery";
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-notificaciones',
  templateUrl: './notificaciones.page.html',
  styleUrls: ['./notificaciones.page.scss'],
})
export class NotificacionesPage{

  listNotificaciones = []
  constructor(private App: AppComponent, private alertController: AlertController, private router: Router) { }


  ionViewDidEnter() {
    this.listNotificaciones = []
    if (this.App.id_User != null) {
      this.getNotificaciones();
    }
  }

  async getNotificaciones() {
    var self = this;
    var data = {
      "id": this.App.id_User
    }
    await $.post(environment.url + "/api/notificaciones_participante/", data).done(function (notificacion) {
      if (!notificacion.error) {
        self.listNotificaciones = notificacion.notificaciones
        for (let i = 0; i < self.listNotificaciones.length; i++) {
          self.listNotificaciones[i].imagen = environment.url + self.listNotificaciones[i].imagen
        }
      }
      else {
        self.alertNotificacion('Sin Notificaciones', notificacion.mensaje)
      }

    })

  }

  async alertNotificacion(msg: string, mensaje: string) {
    const alert = await this.alertController.create({
      header: msg,
      message: mensaje,
      buttons: ['OK']
    });

    await alert.present();
  }

  remover(id_notificacion) {
    var self=this;
    let data = {
      "id_notificacion_participante": id_notificacion,
      "estado":false
    }

    $.ajax({
      url: environment.url + "/api/actualizar_notificacion/",
      data: data,
      type: 'PATCH',
      success: function (notificacion) {
        if (!notificacion.error) {
          self.alertNotificacion("Notificación eliminada", notificacion.mensaje)
        }
        else {
          self.alertNotificacion("Error", notificacion.mensaje)
        }
      }
    });

  }

  async alertDetalle(index) {
    const alert = await this.alertController.create({
      buttons: [{ text: 'Remover', handler: () => { this.remover(this.listNotificaciones[index].id_notificacion_participante) } }, { text: 'Cerrar' }],
      message: `
    <img src="${this.listNotificaciones[index].imagen}" style="width:80%; height:80%; border-radius: 2px">
    <ion-item>
      <ion-text> <b>${this.listNotificaciones[index].titulo} </b> </ion-text>
    </ion-item>
    <ion-item>
      <ion-text> ${this.listNotificaciones[index].descripcion} </ion-text>
    </ion-item>`,

    });
    await alert.present();
  }


}
