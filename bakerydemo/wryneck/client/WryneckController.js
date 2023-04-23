import * as stimulus from "@hotwired/stimulus";

const { Controller } = stimulus;

export class WryneckController extends Controller {
  connect() {
    console.log('wryneck connected!');
  }
}
