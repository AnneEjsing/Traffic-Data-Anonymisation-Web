import { Injectable } from '@angular/core';
import { JwtHelperService } from '@auth0/angular-jwt';
import { Token } from '../_models/token';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable()
export class AuthService {
  constructor(
    public jwtHelper: JwtHelperService,
    private http: HttpClient
  ) { }

  readonly dispatcherUrl = "http://localhost:443/";

  public isAuthenticatedAdmin(): Observable<boolean> {
    return this.getRole().pipe(map(value => {
      if (this != null && value === "admin") {
        return true;
      } else {
        return false;
      }
    }));
  }

  public isAuthenticated(): Observable<boolean> {
    const token = localStorage.getItem('session_token');
    if (token != null) {
      const resolved = this.http
        .get<boolean>(this.dispatcherUrl + 'auth/authenticate', this.constructHttpOptions());

      return resolved.pipe(map(value => {
        if (value === true) {
          return true;
        } else {
          localStorage.clear();
          return false;
        }
      }));
    } else {
      localStorage.clear();
      return of(false);
    }
  }

  public getRole(): Observable<string> {
    return this.isAuthenticated().pipe(map(val => {
      if (val) {
        const token = localStorage.getItem('session_token');
        const decoded: Token = this.jwtHelper.decodeToken(token);
        if (decoded == null) {
          return null;
        }
        return decoded.rights;
      } else {
        return null;
      }
    }));
  }

  public getEmail(): Observable<string> {
    return this.isAuthenticated().pipe(map(val => {
      if (val) {
        const token = localStorage.getItem('session_token');
        const decoded: Token = this.jwtHelper.decodeToken(token);
        if (decoded == null) {
          return null;
        }
        return decoded.rights;
      } else {
        return null;
      }
    }));
  }

  public getId(): Observable<string> {
    return this.isAuthenticated().pipe(map(val => {
      if (val) {
        const token = localStorage.getItem('session_token');
        const decoded: Token = this.jwtHelper.decodeToken(token);
        if (decoded == null) {
          return null;
        }
        return decoded.sub;
      } else {
        return null;
      }
    }));
  }

  constructHttpOptions() {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + localStorage.getItem('session_token')
      })
    };

    return httpOptions;
  }
}