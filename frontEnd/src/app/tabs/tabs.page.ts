import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AlertController } from '@ionic/angular';
import { AppComponent } from "../app.component";

@Component({
  selector: 'app-tabs',
  templateUrl: 'tabs.page.html',
  styleUrls: ['tabs.page.scss']
})

export class TabsPage {
  listTabs: any;
  num_notificaciones:number;
  constructor(private alertController: AlertController,
    private router: Router, private App: AppComponent) {
    this.listTabs = this.App.listTabs;
    this.num_notificaciones=0;
  }

  verificar(index: number) {
    if (this.listTabs[index].disable) this.alertLogin();
  }

  async alertLogin() {
    const alert = await this.alertController.create({
      header: 'Para continuar regístrese o inicie sesión',
      message: '¿Desea registrarse o iniciar sesión?',
      backdropDismiss: false,
      buttons: [{text: 'NO', handler: () => {
        this.router.navigate(["/educ/home/"]);
      }}, {
          text: 'SI', handler: () => {
            this.router.navigate(["/login"]);
          }
        }]
    });
    await alert.present();
  }

}
