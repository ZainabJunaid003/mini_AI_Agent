import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() => runApp(const MaterialApp(home: ChatPage()));

class ChatPage extends StatefulWidget {
  const ChatPage({super.key});
  @override
  State<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  // 10.0.2.2 = your PC's localhost, as seen from the Android emulator
  static const baseUrl = 'http://10.0.2.2:8000';
  final controller = TextEditingController();
  final List<Map<String, String>> messages = [];
  bool loading = false;

  Future<void> send() async {
    final text = controller.text.trim();
    if (text.isEmpty) return;
    setState(() {
      messages.add({'role': 'user', 'text': text});
      loading = true;
    });
    controller.clear();
    try {
      final res = await http.post(
        Uri.parse('$baseUrl/chat'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'message': text}),
      );
      final data = jsonDecode(res.body);
      setState(() => messages.add({'role': 'bot', 'text': data['reply']}));
    } catch (e) {
      setState(() => messages.add({'role': 'bot', 'text': 'Error: $e'}));
    }
    setState(() => loading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Mini AI Agent')),
      body: Column(children: [
        Expanded(
          child: ListView.builder(
            padding: const EdgeInsets.all(8),
            itemCount: messages.length,
            itemBuilder: (_, i) {
              final m = messages[i];
              final isUser = m['role'] == 'user';
              return Align(
                alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                child: Container(
                  margin: const EdgeInsets.symmetric(vertical: 4),
                  padding: const EdgeInsets.all(12),
                  constraints: const BoxConstraints(maxWidth: 280),
                  decoration: BoxDecoration(
                    color: isUser ? Colors.blue[100] : Colors.grey[300],
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(m['text']!),
                ),
              );
            },
          ),
        ),
        if (loading) const LinearProgressIndicator(),
        Padding(
          padding: const EdgeInsets.all(8),
          child: Row(children: [
            Expanded(
              child: TextField(
                controller: controller,
                onSubmitted: (_) => send(),
                decoration: const InputDecoration(
                    hintText: 'Ask something...', border: OutlineInputBorder()),
              ),
            ),
            IconButton(icon: const Icon(Icons.send), onPressed: send),
          ]),
        ),
      ]),
    );
  }
}