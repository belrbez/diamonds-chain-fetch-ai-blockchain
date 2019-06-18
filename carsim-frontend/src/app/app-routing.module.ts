import { NgModule } from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {MapComponent} from './map/map-component/map.component';

const routes: Routes = [
  { path: 'map/:id', component: MapComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
