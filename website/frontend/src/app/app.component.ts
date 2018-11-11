import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent{
  title = 'app';
  //queryname: String;

  titleData: JSON;
  authorData: JSON;

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
    this.authorData = data as JSON;
    })
  }

  searchTitle(titleName){
    //alert("this is title");
    this.httpClient.post('http://127.0.0.1:5008/'+"title",{"bookname":titleName}).subscribe(data => {
    this.titleData = data as JSON;
    })
  }
}
