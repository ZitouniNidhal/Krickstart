import * as vscode from 'vscode';
import { CliRunner } from './cliRunner';

export function activate(context: vscode.ExtensionContext) {
    const runner = new CliRunner();

    const upCommand = vscode.commands.registerCommand('devspeed.up', async () => {
        if (!(await runner.checkInstallation())) {
            vscode.window.showErrorMessage('DevSpeed CLI not found. Please install it via: pip install devspeed');
            return;
        }
        await runner.runCommand('devspeed up');
        vscode.window.showInformationMessage('DevSpeed: Environment startup initiated. Check the Output panel for details.');
    });

    const initCommand = vscode.commands.registerCommand('devspeed.init', async () => {
        if (!(await runner.checkInstallation())) {
            vscode.window.showErrorMessage('DevSpeed CLI not found. Please install it via: pip install devspeed');
            return;
        }
        // For init, we use the terminal to allow interactive input
        const terminal = vscode.window.createTerminal('DevSpeed Init');
        terminal.sendText('devspeed create');
        terminal.show();
    });

    const doctorCommand = vscode.commands.registerCommand('devspeed.doctor', async () => {
        if (!(await runner.checkInstallation())) {
            vscode.window.showErrorMessage('DevSpeed CLI not found. Please install it via: pip install devspeed');
            return;
        }
        await runner.runCommand('devspeed doctor');
    });

    const cleanupCommand = vscode.commands.registerCommand('devspeed.cleanup', async () => {
        if (!(await runner.checkInstallation())) {
            vscode.window.showErrorMessage('DevSpeed CLI not found. Please install it via: pip install devspeed');
            return;
        }
        await runner.runCommand('devspeed cleanup');
        vscode.window.showInformationMessage('DevSpeed: Cleanup complete.');
    });

    context.subscriptions.push(upCommand, initCommand, doctorCommand, cleanupCommand);
}

export function deactivate() {}