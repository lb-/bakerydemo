import * as stimulus from "@hotwired/stimulus";

const { Controller } = stimulus;

export class WryneckController extends Controller {
  static targets = ['input'];

  connect() {
    console.log('wryneck connected!', this.inputTarget);
  }
}
