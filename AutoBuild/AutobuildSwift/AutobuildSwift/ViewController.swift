//
//  ViewController.swift
//  AutobuildSwift
//
//  Created by 刘通超 on 2016/10/27.
//  Copyright © 2016年 北京京师乐学教育科技有限公司. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    @IBOutlet weak var lab: UILabel!
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        self.lab.text = "Debug";
        self.lab.backgroundColor = UIColor.red
        #if DEBUG // 判断是否在测试环境下
            self.lab.text = "Swift-Debug";
            self.lab.backgroundColor = UIColor.green
        #else
            self.lab.text = "Swift-Release";
            self.lab.backgroundColor = UIColor.red
            
        #endif
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

