//
//  ViewController.m
//  AutoBuildProject
//
//  Created by 刘通超 on 2016/10/26.
//  Copyright © 2016年 北京京师乐学教育科技有限公司. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()
@property (weak, nonatomic) IBOutlet UILabel *lab;

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
#ifdef DEBUG
    self.lab.text = @"Debug";
    self.lab.backgroundColor = [UIColor greenColor];
#else
    self.lab.text = @"Release";
    self.lab.textColor = [UIColor whiteColor];
    self.lab.backgroundColor = [UIColor redColor];
#endif
}


- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}


@end
