import {Injectable} from '@angular/core';
import {Account} from '../model/account';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Trip} from '../model/trip';

@Injectable({
  providedIn: 'root'
})
export class AccountService {

  private accounts: Account[];
  public map: any;
  public account: Account | null;

  constructor(
    private http: HttpClient) {
    this.accounts = [
      {
        id: 'id1',
        name: 'Steve Gabe',
        canBeDriver: true
      } as Account,
      {
        id: 'id2',
        name: 'Samantha Smith',
        canBeDriver: true
      } as Account
    ];
  }

  public getAccount(id: string): Promise<Account | null> {
    return new Promise<Account | null>((resolve, reject) => {

      this.http.get(`?id=${id}`).subscribe((account: Account | null) => {
        if (account != null) {
          resolve(account);
        } else {
          resolve(this.getAccountInternal(id));
        }
      }, () => {
        resolve(this.getAccountInternal(id));
      });

    });
  }

  public getTrip(accountId: string, tripId: string): Promise<Trip | null> {
    return new Promise<Trip | null>((resolve, reject) => {

        this.http.get(`api/trips/${tripId}`).subscribe((trip: Trip | null) => {
          if (trip != null) {
            resolve(trip);
          } else {
            resolve(null);
          }
        }, () => {
          resolve(null);
        });

    });
  }

  private getAccountInternal(id: string): Account | null {
    const found = this.accounts.filter(account => account.id === id);
    if (found.length > 0) {
      return found[0];
    }
    return null;
  }

  public drive(account: Account, pick: any): Observable<Trip> {
    return this.http.post<Trip>('api/trips', {
      account_id: account.id,
      name: account.name,
      start: {
        longitude: pick.longitudeFrom,
        latitude: pick.latitudeFrom
      },
      end: {
        longitude: pick.longitudeTo,
        latitude: pick.latitudeTo
      },
      can_be_driver: account.canBeDriver
    });
  }

  public tripState(tripId: string) {
    return this.http.get('trips/' + tripId);
  }
}
