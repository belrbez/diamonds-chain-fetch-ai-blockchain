import {Injectable} from '@angular/core';
import {Account} from '../model/account';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AccountService {

  private accounts: Account[];

  constructor(
    private http: HttpClient) {
    this.accounts = [
      {
        id: 'id1',
        name: 'Steve Gabe'
      } as Account,
      {
        id: 'id2',
        name: 'Samantha Smith'
      } as Account
    ];
  }

  public getAccount(id: string): Account | null {
    const found = this.accounts.filter(account => account.id === id);
    if (found.length > 0) {
      return found[0];
    }
    return null;
  }

  public drive(account: Account, pick: any): Observable<string> {
    return this.http.post<string>('trips', {
      id: account.id,
      name: account.name,
      start: {
        longitude: pick.longitudeFrom,
        latitude: pick.latitudeFrom
      },
      end: {
        longitude: pick.longitudeTo,
        latitude: pick.latitudeTo
      },
      canBeDriver: account.canBeDriver
    })
  }

  public tripState(tripId: string) {
    return this.http.get('trips/' + tripId);
  }
}
