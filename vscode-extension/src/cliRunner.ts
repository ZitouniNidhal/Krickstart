import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as pathlib from 'path';

export class CliRunner {
    private outputChannel: vscode.OutputChannel;

    constructor() {
        this.outputChannel = vscode.window.createOutputChannel('DevSpeed');
    }

    async runCommand(command: string): Promise<void> {
        this.outputChannel.show(true);
        this.outputChannel.appendLine(`Executing: ${command}...`);

        return new Promise((resolve, reject) => {
            const process = exec(command, (error, stdout, stderr) => {
                if (stdout) this.outputChannel.appendLine(stdout);
                if (stderr) this.outputChannel.appendLine(`Error: ${stderr}`);
                
                if (error) {
                    vscode.window.showErrorMessage(`DevSpeed Error: ${error.message}`);
                    reject(error);
                } else {
                    resolve();
                }
            });

            // Stream output in real-time
            process.stdout.on('data', (data) => {
                this.outputChannel.append(data.toString());
            });
            process.stderr.on('data', (data) => {
                this.outputChannel.append(`[stderr] ${data.toString()}`);
            });
        });
    }

    async checkInstallation(): Promise<boolean> {
        return new Promise((resolve) => {
            exec('devspeed --version', (error) => {
                resolve(!error);
            });
        });
    }
}