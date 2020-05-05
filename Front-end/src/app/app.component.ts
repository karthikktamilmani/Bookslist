import { Component } from '@angular/core';
import{ GlobalConstants } from './globalconstants';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.sass']
})
export class AppComponent {
  title = GlobalConstants.siteTitle ;

}
