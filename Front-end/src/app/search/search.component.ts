import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import{ GlobalConstants } from '../globalconstants';
import * as $ from 'jquery';



@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.sass']
})
export class SearchComponent implements OnInit {
  searchForm: FormGroup;
  isLoaded = false;
  apiResp: any;
  constructor(private fb:FormBuilder, private httpClient: HttpClient) { }

  ngOnInit(): void {
    this.searchForm = this.fb.group({
      type : [ 'Title' , Validators.required],
      query : ['', [Validators.required, Validators.minLength(3)]]
    });
  }

  getBooks()
  {
    console.log("hii")
    this.isLoaded = false;
    if (this.searchForm.invalid) {
    }
    else{
      console.log(this.searchForm.value);
    this.httpClient.get(GlobalConstants.apiURL+'/getBooks?'+$.param(this.searchForm.value)).subscribe((res)=>{
      this.isLoaded = true;
      console.log("byeee");
      console.log(res);
      this.apiResp = res;
    },(err)=>{

    });
  }
}

}
