import { Component, OnInit } from '@angular/core';
import { Input } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import{ GlobalConstants } from '../globalconstants';
import * as $ from 'jquery';

@Component({
  selector: 'app-listing',
  templateUrl: './listing.component.html',
  styleUrls: ['./listing.component.sass']
})
export class ListingComponent implements OnInit {
  @Input() booksAndNotesResp;
  notesList = [];
  booksList = [];

  constructor(private httpClient: HttpClient) { }

  ngOnInit(): void {
    if (this.booksAndNotesResp != null || this.booksAndNotesResp != "[]")
    {
      if("books" in this.booksAndNotesResp){
        this.booksList = this.booksAndNotesResp["books"];
      }

      if("notes" in this.booksAndNotesResp){
        this.notesList = this.booksAndNotesResp["notes"];
      }
    }
  }

  addNotesLink(book){
    book.isAdd = true;
  }

  addNotes(notes,book)
  {
    console.log(notes);
    // console.log(bookTitle);
      let noteItems = this.notesList[book.Title] != null ? this.notesList[book.Title] : [];
      const dataItems = {
        query : book.Title,
        notes : notes
      };
      this.httpClient.post(GlobalConstants.apiURL+'/submitNotes?',dataItems).subscribe((res)=>{
        console.log("hiiii")
        noteItems.push(notes);
        this.notesList[book.Title] = noteItems;
        book.isAdd = false;
      });

  }

}
