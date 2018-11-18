import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent{
  title = 'app';

  serverData: string;

  constructor(private httpClient: HttpClient) {
  }

  ngOnInit() {
  }

  test(queryname){
    alert(typeof(queryname));
  }

  searchAuthor(authorName){
    //alert("This is author");
    this.httpClient.post('http://127.0.0.1:5008/'+"author",{"authorname":authorName}).subscribe(data => {
    //this.authorData = data["respond"];
    var respond = data["respond"];
    this.serverData = respond.replace(/<br\s*[\/]?>/gi, "\n");
    })
  }

  searchTitle(titleName){
    //alert("this is title");
    this.httpClient.post('http://127.0.0.1:5008/'+"title",{"bookname":titleName}).subscribe(data => {
    //this.titleData = data["respond"];
    var respond = data["respond"];
    this.serverData = respond.replace(/<br\s*[\/]?>/gi, "\n");
    })
  }
}
