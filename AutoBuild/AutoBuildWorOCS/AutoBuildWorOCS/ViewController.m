//
//  ViewController.m
//  AutoBuildWorOCS
//
//  Created by 刘通超 on 2016/10/27.
//  Copyright © 2016年 北京京师乐学教育科技有限公司. All rights reserved.
//

#import "ViewController.h"
#import "AutoBuildWorOCS-Swift.h"

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
    
    
    NSURL* url = [[NSURL alloc] initWithString:@"http://localhost:8080"];
    SocketIOClient* socket = [[SocketIOClient alloc] initWithSocketURL:url config:@{@"log": @YES, @"forcePolling": @YES}];
    
    [socket on:@"connect" callback:^(NSArray* data, SocketAckEmitter* ack) {
        NSLog(@"socket connected");
    }];
    
    [socket on:@"currentAmount" callback:^(NSArray* data, SocketAckEmitter* ack) {
        double cur = [[data objectAtIndex:0] floatValue];
        
        [socket emitWithAck:@"canUpdate" with:@[@(cur)]](0, ^(NSArray* data) {
            //            [socket emit:@"update" withItems:@[@{@"amount": @(cur + 2.50)}]];
        });
        
        [ack with:@[@"Got your currentAmount, ", @"dude"]];
    }];
    
    [socket connect];
}


- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}


@end
