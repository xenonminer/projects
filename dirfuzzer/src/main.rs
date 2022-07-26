use std::env;
use std::fs;
use std::io::Read;
use error_chain::error_chain;
use device_query::{DeviceQuery, DeviceState, Keycode};

fn help() {

    println!("dirfuzzer's help list\n");
    println!("-u to specify FULL url (with the http:// or https://");
    println!("-w to specify wordlist");
    println!("-v to only output valid directories");
    println!("\nYou can also press any key during the program duration to check the status of the program\n");
    println!("EXAMPLES");
    println!(".\\dirfuzzer.exe -v -u https://google.com -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt");
    println!(".\\dirfuzzer.exe -u https://google.com -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt\n");

}

error_chain! {
    foreign_links {
        Io(std::io::Error);
        HttpRequest(reqwest::Error);
    }
}

fn request(url: &String, wordlist: String, v_flag: bool) {

    let mut line_counter = 0;

    for line in wordlist.lines() { // loop through all lines in the file

        let url_to_send = url.to_owned() + "/" + line; //create full url to send

        let mut res = reqwest::blocking::get(url_to_send)
            .expect("Broken");

        let mut body = String::new();
        res.read_to_string(&mut body);

        if v_flag {
            if res.status().to_string().contains("200") {
                println!("/{}{}(Size: {}){}[Status: {}]", line, " ".repeat(25-line.len()), body.len(), " ".repeat(15-6-body.len().to_string().len()), res.status()); // return formatted output
            }
        } else {
            println!("/{}{}(Size: {}){}[Status: {}]", line, " ".repeat(25-line.len()), body.len(), " ".repeat(15-6-body.len().to_string().len()), res.status()); // return formatted output
        }

        line_counter += 1;

        let device_state = DeviceState::new();
        let keys: Vec<Keycode> = device_state.get_keys();
        if !keys.is_empty(){ // check for any keyboard input to run status
            println!("{}/{}   {}% Done", line_counter, wordlist.lines().count(), line_counter/wordlist.lines().count());
        }

    }

    println!("");

}
fn main() {
    let args: Vec<String> = env::args().collect(); // collect the args into an array

    if args.len() <= 1 {
        println!("Run with --help to print more information on using the program."); // make sure the program is run with arguments
    } else if (!args.iter().any(|i| i=="-u") || !args.iter().any(|i| i=="-w"))  && !args.iter().any(|i| i=="--help") { // make sure the program is run with the right arguments
        println!("Run with --help to print more information on using the program.");
    } else if args[1] == "--help" {
        help();
    } else {

        let url_index = args.iter().position(|x| x == "-u").unwrap() + 1; // get index of the url argument
        let wordlist_index = args.iter().position(|x| x == "-w").unwrap() + 1; // get index of the wordlist argument

        let wordlist_contents = fs::read_to_string(&args[wordlist_index]) // read file
            .expect("Something went wrong reading the file");
        
        let mut v_flag = false;

        if args.iter().any(|x| x =="-v") { // check if -v is set
            v_flag = true;
        }

        request(&args[url_index], wordlist_contents, v_flag);

    }

}